#!/usr/bin/env python3
"""
Master test runner for all MCTS tests
Run this to validate your complete MCTS implementation
"""

import sys
import traceback

def run_test_file(filename, description):
    """Run a test file and handle errors gracefully"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    
    try:
        # Import and run the test
        if filename == "test_mcts_unit.py":
            import test_mcts_unit
        elif filename == "test_mcts_integration.py":
            import test_mcts_integration
            test_mcts_integration.run_integration_tests()
        
        print(f"✅ {description} PASSED")
        return True
        
    except Exception as e:
        print(f"❌ {description} FAILED")
        print(f"Error: {e}")
        traceback.print_exc()
        return False

def main():
    print("🚀 COMPREHENSIVE MCTS TESTING SUITE")
    print("This will test your MCTS implementation thoroughly")
    
    tests = [
        ("test_mcts_unit.py", "Unit Tests - Individual Components"),
        ("test_mcts_integration.py", "Integration Tests - Algorithm Behavior")
    ]
    
    passed = 0
    total = len(tests)
    
    for filename, description in tests:
        if run_test_file(filename, description):
            passed += 1
    
    print(f"\n{'='*60}")
    print(f"🏆 FINAL RESULTS: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Your MCTS implementation is working correctly!")
        print("\nYour MCTS is ready for:")
        print("  • Production use")
        print("  • Academic presentations") 
        print("  • Algorithm comparisons")
        print("  • Further research")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        print("Debug the failing components before proceeding.")
        
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
