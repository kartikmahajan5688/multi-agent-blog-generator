"""
Test script for Multi-Agent Blog Generator API
"""

import requests
import json
import time
from typing import Dict

# Configuration
API_URL = "http://localhost:8000"
GENERATE_ENDPOINT = f"{API_URL}/generate"
HEALTH_ENDPOINT = f"{API_URL}/health"


def test_health_check():
    """Test the health check endpoint"""
    print("\n🔍 Testing Health Check...")
    try:
        response = requests.get(HEALTH_ENDPOINT)
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False


def test_blog_generation(topic: str, tone: str = "professional", length: str = "medium"):
    """Test blog generation with given parameters"""
    print(f"\n📝 Testing Blog Generation...")
    print(f"   Topic: {topic}")
    print(f"   Tone: {tone}")
    print(f"   Length: {length}")

    payload = {
        "topic": topic,
        "tone": tone,
        "length": length
    }

    try:
        start_time = time.time()
        response = requests.post(
            GENERATE_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        end_time = time.time()

        elapsed_time = end_time - start_time

        if response.status_code == 200:
            data = response.json()
            print(
                f"✅ Blog generated successfully in {elapsed_time:.2f} seconds!")

            # Display results
            print("\n" + "="*80)
            print("🔍 RESEARCH OUTPUT:")
            print("="*80)
            print(data['research'][:500] +
                  "..." if len(data['research']) > 500 else data['research'])

            print("\n" + "="*80)
            print("✍️  DRAFT OUTPUT:")
            print("="*80)
            print(data['draft'][:500] + "..." if len(data['draft'])
                  > 500 else data['draft'])

            print("\n" + "="*80)
            print("🎯 FINAL BLOG OUTPUT:")
            print("="*80)
            print(data['final_blog'][:500] +
                  "..." if len(data['final_blog']) > 500 else data['final_blog'])
            print("\n" + "="*80)

            return True
        else:
            print(f"❌ Generation failed with status {response.status_code}")
            print(f"   Error: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Generation error: {e}")
        return False


def test_different_tones():
    """Test different tone options"""
    print("\n🎨 Testing Different Tones...")
    tones = ["professional", "casual", "technical", "friendly"]

    for tone in tones:
        print(f"\n--- Testing {tone.upper()} tone ---")
        test_blog_generation(
            topic="Benefits of Remote Work",
            tone=tone,
            length="short"
        )
        time.sleep(2)  # Small delay between requests


def test_different_lengths():
    """Test different length options"""
    print("\n📏 Testing Different Lengths...")
    lengths = ["short", "medium", "long"]

    for length in lengths:
        print(f"\n--- Testing {length.upper()} length ---")
        test_blog_generation(
            topic="Cloud Computing Trends",
            tone="professional",
            length=length
        )
        time.sleep(2)


def test_error_handling():
    """Test error handling with invalid inputs"""
    print("\n⚠️  Testing Error Handling...")

    # Test with empty topic
    print("\nTest 1: Empty topic")
    try:
        response = requests.post(
            GENERATE_ENDPOINT,
            json={"topic": "", "tone": "professional", "length": "medium"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test with invalid tone
    print("\nTest 2: Invalid tone")
    try:
        response = requests.post(
            GENERATE_ENDPOINT,
            json={"topic": "Test", "tone": "invalid_tone", "length": "medium"}
        )
        print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"   Error: {e}")


def run_all_tests():
    """Run all test suites"""
    print("=" * 80)
    print("🚀 MULTI-AGENT BLOG GENERATOR - TEST SUITE")
    print("=" * 80)

    # Check if API is running
    print("\n📡 Checking API availability...")
    try:
        response = requests.get(API_URL, timeout=5)
        print("✅ API is running!")
    except Exception as e:
        print(f"❌ Cannot connect to API at {API_URL}")
        print(f"   Error: {e}")
        print("\n💡 Make sure to start the API server with: python main.py")
        return

    # Run test suites
    tests = [
        ("Health Check", test_health_check),
        ("Basic Blog Generation", lambda: test_blog_generation(
            "The Impact of AI on Education")),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*80}")
        print(f"Running: {test_name}")
        print('='*80)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))

    # Print summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
    print("="*80)


def interactive_test():
    """Interactive testing mode"""
    print("\n🎮 INTERACTIVE TEST MODE")
    print("="*80)

    while True:
        print("\nOptions:")
        print("1. Generate a blog post")
        print("2. Test different tones")
        print("3. Test different lengths")
        print("4. Test error handling")
        print("5. Run all tests")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            topic = input("Enter blog topic: ")
            tone = input(
                "Enter tone (professional/casual/technical/friendly): ") or "professional"
            length = input("Enter length (short/medium/long): ") or "medium"
            test_blog_generation(topic, tone, length)
        elif choice == "2":
            test_different_tones()
        elif choice == "3":
            test_different_lengths()
        elif choice == "4":
            test_error_handling()
        elif choice == "5":
            run_all_tests()
        elif choice == "6":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_test()
    else:
        run_all_tests()

    print("\n💡 Tip: Run with --interactive flag for interactive mode")
    print("   Example: python test_api.py --interactive")
