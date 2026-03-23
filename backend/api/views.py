from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from dotenv import load_dotenv 
load_dotenv("backend/.env")
from groq import Groq 


DEBUG = os.getenv("DEBUG") == "True"

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message")

            completion = client.chat.completions.create(
               model="llama-3.1-8b-instant",
                messages=[
                     {"role": "system", "content": "You are a friendly and casual assistant. Talk like a human, not like a robot."},
                    {"role": "user", "content": message}]
            )

            reply = completion.choices[0].message.content

            return JsonResponse({"reply": reply})

        except Exception as e:
            return JsonResponse({"reply": str(e)})  
    
    # ✅ Handle GET request
    return JsonResponse({"message": "API is working. Use POST request."})