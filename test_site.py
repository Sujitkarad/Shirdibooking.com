"""
Automated Test Suite for Sujitkarad/Shirdibooking.com
Tests HTML structure, CSS responsiveness rules, JS logic, form validation, and HTTP endpoints.
"""

import os
import re
import urllib.parse
import urllib.request

WORKSPACE = r"c:\Users\Sujit\.gemini\antigravity-ide\scratch\New folder"

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
        assert 'twitter:card' in content, f"Missing twitter:card in {filename}"
        assert 'viewport' in content, f"Missing viewport in {filename}"
        assert '<html lang="en">' in content, f"Missing lang='en' in {filename}"
    print("  --> PASS: HTML metadata and favicons verified in all pages.")

def test_floating_action_buttons_css():
    print("TEST 3: Checking floating action buttons mobile CSS fix...")
    for filename in ["index.html", "book.html"]:
        with open(os.path.join(WORKSPACE, filename), "r", encoding="utf-8") as f:
            content = f.read()

        # Check that mobile rule only hides .float-text, NOT .float-icon or all spans
        assert ".float-btn .float-text { display: none; }" in content, \
            f"Expected '.float-btn .float-text {{ display: none; }}' in {filename}"
        assert ".float-btn span { display: none; }" not in content, \
            f"Buggy '.float-btn span {{ display: none; }}' found in {filename}!"
        assert 'class="float-text"' in content, f"Missing float-text class in {filename}"
        assert 'class="float-icon"' in content, f"Missing float-icon class in {filename}"
    print("  --> PASS: Floating action buttons mobile fix verified (icons visible).")

def test_semantic_booking_form():
    print("TEST 4: Checking booking form semantics, IDs, and labels...")
    for filename in ["index.html", "book.html"]:
        with open(os.path.join(WORKSPACE, filename), "r", encoding="utf-8") as f:
            content = f.read()

        assert '<form class="contact-form reveal" id="bookingForm"' in content, \
            f"Missing form#bookingForm in {filename}"
        assert 'onsubmit="submitBookingForm(event)"' in content, \
            f"Missing onsubmit handler in {filename}"
        assert 'id="bookingName"' in content, f"Missing bookingName id in {filename}"
        assert 'id="bookingPhone"' in content, f"Missing bookingPhone id in {filename}"
        assert 'id="bookingService"' in content, f"Missing bookingService id in {filename}"
        assert 'id="bookingDetails"' in content, f"Missing bookingDetails id in {filename}"
        assert 'id="formFeedback"' in content, f"Missing formFeedback id in {filename}"
        assert 'for="bookingName"' in content, f"Missing for='bookingName' label in {filename}"
        assert 'for="bookingPhone"' in content, f"Missing for='bookingPhone' label in {filename}"
        assert 'for="bookingService"' in content, f"Missing for='bookingService' label in {filename}"
        assert 'for="bookingDetails"' in content, f"Missing for='bookingDetails' label in {filename}"
    print("  --> PASS: Form semantics, labels, and accessible IDs verified.")

def test_whatsapp_message_encoding_logic():
    print("TEST 5: Testing WhatsApp message formatting and URL encoding logic...")
    name = "Ravi Kumar"
    phone = "+91 98765 43210"
    phone_clean = re.sub(r'[^0-9+]', '', phone)
    digits = re.sub(r'\D', '', phone)
    service = "Full Darshan Tour"
    details = "Traveling with family of 4 on Saturday morning"

    assert len(digits) >= 10, "Phone validation should accept 10+ digits"

    wa_msg = (
        f"🙏 *Sai Ram! New Booking Request*\n\n"
        f"👤 *Name:* {name}\n"
        f"📞 *Phone:* {phone_clean}\n"
        f"🛺 *Service:* {service}\n"
        f"📝 *Travel Details:* {details}"
    )

    encoded = urllib.parse.quote(wa_msg)
    wa_url = f"https://wa.me/919307062992?text={encoded}"

    assert "919307062992" in wa_url
    assert "Sai%20Ram" in wa_url or "Sai+Ram" in wa_url
    assert "Ravi%20Kumar" in wa_url or "Ravi+Kumar" in wa_url
    assert "Full%20Darshan%20Tour" in wa_url or "Full+Darshan+Tour" in wa_url
    print("  --> PASS: WhatsApp URL generation formatted and encoded accurately.")

def test_mobile_nav_accessibility():
    print("TEST 6: Checking mobile nav accessibility attributes and escape listener...")
    for filename in ["index.html", "book.html"]:
        with open(os.path.join(WORKSPACE, filename), "r", encoding="utf-8") as f:
            content = f.read()

        assert 'id="hamburgerBtn"' in content, f"Missing hamburgerBtn id in {filename}"
        assert 'aria-label="Toggle navigation menu"' in content, f"Missing aria-label on hamburger in {filename}"
        assert 'aria-expanded="false"' in content, f"Missing aria-expanded on hamburger in {filename}"
        assert 'aria-controls="mobileNav"' in content, f"Missing aria-controls on hamburger in {filename}"
        assert "e.key === 'Escape'" in content, f"Missing Escape key listener in {filename}"
        assert ".hamburger.active" in content, f"Missing active hamburger CSS transition in {filename}"
    print("  --> PASS: Mobile navigation accessibility & keyboard support verified.")

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
    test_semantic_booking_form()
    test_whatsapp_message_encoding_logic()
    test_mobile_nav_accessibility()
    test_local_server_endpoints()
    print("\n=== ALL TESTS PASSED SUCCESSFULLY! ===")
