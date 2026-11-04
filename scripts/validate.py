#!/usr/bin/env python3
"""Validate the local console worksheet without credentials or network access."""

import json
import re
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = {
    'get_guide', 'get_fax_capabilities', 'prepare_fax', 'get_fax_document',
    'quote_fax', 'send_approved_fax', 'get_fax_status', 'list_faxes',
    'get_fax_balance', 'cancel_fax', 'request_human_review', 'get_review_status',
    'list_inbox', 'read_inbound_fax', 'extract_fax_data',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f'Invalid JSON constant: {value}')


def read_json(name):
    text = (ROOT / name).read_text(encoding='utf-8')
    require(not re.search(r'ffa_(?:test|live)_[A-Za-z0-9]+', text), f'{name}: credential-like value')
    data = json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)
    require(isinstance(data, dict), f'{name}: expected an object')
    check_secrets(data)
    return data


def check_secrets(value):
    if isinstance(value, dict):
        for key, child in value.items():
            require(key.lower() not in {'api_key', 'client_secret', 'access_token', 'refresh_token', 'password'},
                    f'Credential field is not allowed: {key}')
            check_secrets(child)
    elif isinstance(value, list):
        for child in value:
            check_secrets(child)


def text_list(value, minimum, label):
    require(isinstance(value, list) and len(value) >= minimum, f'{label}: needs at least {minimum} entries')
    require(all(isinstance(item, str) and item.strip() for item in value), f'{label}: empty or invalid entry')
    require(len(set(value)) == len(value), f'{label}: duplicate entry')


def validate_icon(path):
    data = path.read_bytes()
    require(len(data) <= 1024 * 1024, 'Icon exceeds 1,024 KB')
    require(data[:8] == b'\x89PNG\r\n\x1a\n', 'Icon must be PNG')
    offset = 8
    chunks = []
    compressed = bytearray()
    header = None
    while offset < len(data):
        require(offset + 12 <= len(data), 'Truncated PNG chunk')
        length = struct.unpack('>I', data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        end = offset + 8 + length
        require(end + 4 <= len(data), 'Truncated PNG payload')
        payload = data[offset + 8:end]
        crc = struct.unpack('>I', data[end:end + 4])[0]
        require(zlib.crc32(kind + payload) & 0xffffffff == crc, 'Invalid PNG checksum')
        if kind == b'IHDR':
            require(not chunks and length == 13, 'Invalid PNG header')
            header = struct.unpack('>IIBBBBB', payload)
        if kind == b'IDAT':
            compressed.extend(payload)
        chunks.append(kind)
        offset = end + 4
        if kind == b'IEND':
            require(length == 0 and offset == len(data), 'Invalid PNG end')
            break
    require(header is not None and header[:2] == (512, 512), 'Icon must be 512 by 512 pixels')
    require(chunks[-1:] == [b'IEND'] and compressed, 'Incomplete PNG')
    # The supplied brand asset is an 8-bit RGB/RGBA, non-interlaced PNG.
    require(header[2] == 8 and header[3] in (2, 6) and header[4:] == (0, 0, 0),
            'Expected an 8-bit RGB/RGBA, non-interlaced brand PNG')
    channels = 3 if header[3] == 2 else 4
    expected_size = 512 * (1 + 512 * channels)
    decoder = zlib.decompressobj()
    pixels = decoder.decompress(bytes(compressed), expected_size + 1)
    require(len(pixels) == expected_size and decoder.eof and not decoder.unused_data,
            'Invalid PNG pixel stream')


def main():
    listing = read_json('listing.json')
    review = read_json('review-cases.json')
    require(listing['format'] == 'local-console-worksheet', 'Do not claim a Google manifest schema')
    require(review['format'] == 'local-review-checklist', 'Invalid review format')
    require(listing['version'] == review['version'], 'Package versions differ')
    require(listing['publisher']['legal_name'] == 'JSB Holdings LLC', 'Publisher mismatch')
    details = listing['app_details']
    require(details['name'] == 'Fax for Agents', 'App name mismatch')
    description = details['description']
    require(isinstance(description, str) and 0 < len(description.split()) < 30, 'Description must be under 30 words')
    require(description.endswith('.') and len(re.findall(r'[.!?]', description)) == 1,
            'Description must be one sentence')
    text_list(details['capabilities'], 3, 'Capabilities')
    prompts = details['example_prompts']
    text_list(prompts, 3, 'Example prompts')
    require(sum(p.startswith('@Fax for Agents ') for p in prompts) >= 2, 'Two prompts must start with @Fax for Agents')
    require(any('Fax for Agents' in p and not p.startswith(('Fax for Agents', '@Fax for Agents')) for p in prompts),
            'One prompt must mention the app naturally after its start')
    public_copy = [description, *details['capabilities'], *prompts]
    for item in public_copy:
        require(not re.match(r'^\s*\d', item), 'Listing entries cannot start with numbers')
        require(';' not in item, 'Listing copy contains a semicolon')
        require(item.isascii(), 'Listing copy must use plain ASCII text')
        require(not re.search(r'\b(price|prices|pricing|free|paid|prepaid|cost|costs|cheap|cheapest|fee|fees|premium|best|leading|seamless)\b', item, re.I),
                'Listing copy contains pricing or promotional language')
    require(all(not p.startswith(('"', "'")) and not p.endswith(('"', "'")) for p in prompts),
            'Example prompts cannot have outer quotation marks')
    for field, url in {
        'terms_of_service_url': 'https://faxforagents.com/terms/',
        'privacy_policy_url': 'https://faxforagents.com/privacy/',
        'website_url': 'https://faxforagents.com/',
    }.items():
        require(details[field] == url, f'Incorrect {field}')
    require(listing['support_url'] == 'https://faxforagents.com/contact/', 'Incorrect support URL')
    require(listing['documentation_url'] == 'https://faxforagents.com/docs/mcp/', 'Incorrect documentation URL')
    require(listing['category']['proposed_value'] == 'Productivity', 'Unexpected proposed category')
    require(listing['category']['status'] == 'operator_confirmation_required', 'Category acceptance is unverified')
    connection = listing['connection']
    for field, expected in {
        'type': 'MCP server', 'endpoint': 'https://mcp.faxforagents.com/mcp',
        'transport': 'Streamable HTTP', 'requires_authorization': True,
        'authorization_model': 'User-delegated (Authorization Code)',
        'client_registration': 'Client ID metadata or Dynamic client registration (recommended)',
        'authorization_server': 'https://api.faxforagents.com', 'pkce_method': 'S256',
    }.items():
        require(connection[field] == expected, f'Incorrect connection field: {field}')
    require(connection['custom_authorization_endpoint'] is None and connection['custom_token_endpoint'] is None,
            'This worksheet uses discovery without custom endpoint overrides')
    require(connection['redirect_uris'] == [], 'Copy redirect URIs privately from the console before deployment')
    domain = listing['domain_verification']
    require(domain['url'] == 'https://mcp.faxforagents.com/.well-known/google-connected-apps', 'Domain challenge host or path mismatch')
    require(domain['http_status'] == 200 and domain['redirects_allowed'] is False, 'Challenge must return 200 without redirects')
    require(domain['recommended_content_type'] == 'application/json', 'Incorrect serving content type')
    availability = listing['availability']
    require(availability['countries_regions'] is None, 'Country availability needs operator confirmation')
    require(availability['languages'] == ['English'], 'Unexpected proposed languages')
    require(availability['products'] == ['Gemini app', 'Search'], 'Unexpected target products')
    require(availability['status'] == 'operator_confirmation_required', 'Availability acceptance is unverified')
    settings = listing['tool_settings']
    require(len(settings) == 15 and {t['name'] for t in settings} == TOOLS, 'Expected exactly the 15 product tools')
    for item in settings:
        require(item['enabled'] is True and item['additional_context'] == [], 'Tools must be enabled without extra context')
        require(type(item['user_confirmation_required']) is bool, 'Confirmation must be boolean')
        if item['name'] in {'send_approved_fax', 'cancel_fax', 'request_human_review'}:
            require(item['user_confirmation_required'], 'Mutation needs the proposed confirmation setting')
    require(listing['testing']['status'] == 'not_run' and review['execution_status'] == 'not_run', 'Do not claim unexecuted tests passed')
    require(listing['testing']['tester_email_lists'] == [], 'Tester identities belong in the console')
    require(review['surface'] == 'Gemini app', 'Review surface mismatch')
    require(len(review['positive']) == 5 and len(review['negative']) == 3, 'Expected five positive and three negative cases')
    ids = []
    for group in ('positive', 'negative'):
        for case in review[group]:
            ids.append(case['id'])
            for field in ('description', 'prompt', 'expected_behavior'):
                require(isinstance(case[field], str) and case[field].strip(), f'Case needs {field}')
            text_list(case['preconditions'], 1, 'Case preconditions')
            require(case['result'] == 'not_run', 'Do not claim an unexecuted case passed')
            require(case['prompt'].startswith('@Fax for Agents '), 'Case must target the Gemini app')
            require(isinstance(case['expected_tools'], list) and set(case['expected_tools']) <= TOOLS, 'Unknown expected tool')
            if group == 'negative':
                require('send_approved_fax' in case['forbidden_successful_tools'], 'Negative cases must forbid successful sends')
                require(set(case['forbidden_successful_tools']) <= TOOLS, 'Unknown forbidden tool')
    require(len(set(ids)) == 8, 'Review case IDs must be unique')
    require(details['icon'] == 'assets/icon-512.png', 'Incorrect icon path')
    for filename in ('README.md', 'TESTING.md', 'REQUIREMENTS.md', 'CHANGELOG.md', 'LICENSE', 'SECURITY.md', '.gitignore',
                     listing['testing']['instructions_file'], listing['testing']['review_cases_file']):
        path = (ROOT / filename).resolve()
        require(ROOT in path.parents and path.is_file(), f'Missing or unsafe file: {filename}')
    validate_icon(ROOT / details['icon'])
    print('PASS: worksheet, 15 tools, eight review cases and 512px PNG validated. Authenticated tests remain unrun.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, struct.error, zlib.error) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        sys.exit(1)
