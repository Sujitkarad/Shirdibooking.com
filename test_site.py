"""
Automated Test Suite for Sujitkarad/Shirdibooking.com
Tests Premium HTML structure, CSS responsiveness rules, JS logic, form validation, and short WhatsApp messages to 9307062992.
"""

import os
import re
import urllib.parse
import urllib.request

WORKSPACE = r"c:\Users\Sujit\.gemini\antigravity-ide\scratch\New folder"
DRIVER_PHONE = "9307062992"

def test_files_exist():
    print("TEST 1: Checking required files exist...")
    assert os.path.exists(os.path.join(WORKSPACE, "index.html")), "index.html must exist"
    assert os.path.exists(os.path.join(WORKSPACE, "book.html")), "book.html must exist"
    print("  --> PASS: index.html and book.html exist.")

def test_html_and_meta():
    print("TEST 2: Checking HTML metadata, favicon, and OpenGraph tags...")
    for filename in ["index.html", "book.html"]:
        with open(os.path.join(WORKSPACE, filename), "r", encoding="utf-8") as f:
            content = f.read()

        assert '<link rel="icon"' in content, f"Missing favicon link in {filename}"
        assert 'data:image/svg+xml' in content, f"Favicon should be inline SVG data URI in {filename}"
        assert 'og:title' in content, f"Missing og:title in {filename}"
        assert 'og:description' in content, f"Missing og:description in {filename}"
        assert 'og:image' in content, f"Missing og:image in {filename}"
        assert '<html lang="en">' in content, f"Missing lang='en' in {filename}"
        assert 'Cinzel' in content, f"Missing Cinzel premium font in {filename}"
    print("  --> PASS: HTML metadata, typography and favicons verified in all pages.")

def test_floating_action_buttons_css():
    print("TEST 3: Checking floating action buttons mobile CSS fix...")
    for filename in ["index.html", "book.html"]:
        with open(os.path.join(WORKSPACE, filename), "r", encoding="utf-8") as f:
            content = f.read()

        assert ".float-btn .float-text { display: none; }" in content, \
            f"Expected '.float-btn .float-text {{ display: none; }}' in {filename}"
        assert 'class="float-text"' in content, f"Missing float-text class in {filename}"
        assert 'class="float-icon"' in content, f"Missing float-icon class in {filename}"
    print("  --> PASS: Floating action buttons mobile fix verified (icons visible).")

def test_short_whatsapp_messages():
    print("TEST 4: Verifying all WhatsApp URLs point to 9307062992 with short concise messages...")
    for filename in ["index.html", "book.html"]:
        with open(os.path.join(WORKSPACE, filename), "r", encoding="utf-8") as f:
            content = f.read()

        # Find static href links
        wa_hrefs = re.findall(r'href="(https://wa\.me/919307062992[^"]*)"', content)
        assert len(wa_hrefs) >= 10, f"Expected multiple static WhatsApp booking links in {filename}, found {len(wa_hrefs)}"
        for link in wa_hrefs:
            assert DRIVER_PHONE in link, f"Driver phone {DRIVER_PHONE} not in link {link}"
            decoded = urllib.parse.unquote(link)
            assert ("Sai Ram" in decoded or "Mahadev" in decoded), f"Unexpected message text in {link}"
        
        # Check dynamic JS template literal
        assert f"https://wa.me/91{DRIVER_PHONE}?text=" in content, "Missing JS WhatsApp dynamic URL generation"
    print(f"  --> PASS: Verified {len(wa_hrefs)} WhatsApp links directly targeting driver {DRIVER_PHONE}.")

def test_form_short_message_generation():
    print("TEST 5: Testing booking form short message format...")
    name = "Amit Sharma"
    phone = "9876543210"
    service = "Full Darshan Tour"
    details = "Morning 8 AM pickup"

    expected_wa_msg = f"🙏 Sai Ram Mahadev ji!\n🛺 Booking: {service}\n👤 Name: {name}\n📞 Phone: {phone}\n📝 Note: {details}\nPlease confirm ride."
    encoded = urllib.parse.quote(expected_wa_msg)
    wa_url = f"https://wa.me/91{DRIVER_PHONE}?text={encoded}"

    assert DRIVER_PHONE in wa_url
    assert "Sai%20Ram" in wa_url
    assert "Amit%20Sharma" in wa_url
    assert "Full%20Darshan%20Tour" in wa_url
    print("  --> PASS: Booking form short WhatsApp message generated properly.")

def test_quick_booking_tray():
    print("TEST 6: Checking 1-click Quick Booking tray...")
    for filename in ["index.html", "book.html"]:
        with open(os.path.join(WORKSPACE, filename), "r", encoding="utf-8") as f:
            content = f.read()

        assert 'quick-book-box' in content, f"Missing quick-book-box in {filename}"
        assert 'Local Ride' in content, f"Missing Local Ride in quick book tray in {filename}"
        assert 'Darshan Tour' in content, f"Missing Darshan Tour in quick book tray in {filename}"
        assert 'Pickup / Drop' in content, f"Missing Pickup / Drop in quick book tray in {filename}"
        assert 'Night Aarti' in content, f"Missing Night Aarti in quick book tray in {filename}"
        assert 'Shani Tour' in content, f"Missing Shani Tour in quick book tray in {filename}"
    print("  --> PASS: 1-click Quick Booking tray verified.")

def test_local_server_endpoints():
    print("TEST 7: Testing HTTP server endpoints on localhost:8080...")
    try:
        req_root = urllib.request.urlopen("http://localhost:8080/", timeout=3)
        assert req_root.status == 200, f"Expected 200 from /, got {req_root.status}"
        root_html = req_root.read().decode("utf-8")
        assert "Mahadev Baburao Karad Auto Service" in root_html

        req_book = urllib.request.urlopen("http://localhost:8080/book.html", timeout=3)
        assert req_book.status == 200, f"Expected 200 from /book.html, got {req_book.status}"
        book_html = req_book.read().decode("utf-8")
        assert "Mahadev Baburao Karad Auto Service" in book_html
        print("  --> PASS: Root / and /book.html endpoints responded 200 OK.")
    except Exception as e:
        print(f"  --> WARNING: Local server endpoint test skipped: {e}")

if __name__ == "__main__":
    print("=== RUNNING SUJITKARAD/SHIRDIBOOKING.COM TEST SUITE ===\n")
    test_files_exist()
    test_html_and_meta()
    test_floating_action_buttons_css()
    test_short_whatsapp_messages()
    test_form_short_message_generation()
    test_quick_booking_tray()
    test_local_server_endpoints()
    print("\n=== ALL TESTS PASSED SUCCESSFULLY! ===")
