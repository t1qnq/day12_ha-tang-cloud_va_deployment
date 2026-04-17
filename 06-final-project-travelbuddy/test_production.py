import urllib.request
import json
import time

URL = "http://localhost:8081/chat"
API_KEY = "travel-secret-123"

def post_chat(message, session_id=None):
    data = json.dumps({
        "message": message,
        "session_id": session_id
    }).encode("utf-8")
    
    req = urllib.request.Request(URL, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-API-Key", API_KEY)
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}

def run_test():
    print("🚀 Testing Production TravelBuddy...")
    
    # 1. Câu hỏi đầu tiên
    print("\n[Request 1]")
    r1 = post_chat("Tôi muốn đi du lịch Đà Nẵng, có chuyến bay nào không?")
    print(f"Agent: {r1.get('response', 'Error')}")
    print(f"Session ID: {r1.get('session_id')}")
    print(f"Served by: {r1.get('served_by')}")
    
    sess_id = r1.get('session_id')
    
    # 2. Câu hỏi tiếp theo (Nhớ ngữ cảnh)
    print("\n[Request 2 - Context Check]")
    r2 = post_chat("Còn khách sạn thì sao? Giá dưới 2 triệu nhé.", sess_id)
    print(f"Agent: {r2.get('response', 'Error')}")
    print(f"Served by: {r2.get('served_by')}")
    
    # 3. Security Check (Wrong API Key)
    print("\n[Security Check - Invalid Key]")
    req_fail = urllib.request.Request(URL, data=b'{}', method="POST")
    req_fail.add_header("X-API-Key", "wrong-key")
    try:
        urllib.request.urlopen(req_fail)
    except Exception as e:
        print(f"Expected Error: {e}")

if __name__ == "__main__":
    run_test()
