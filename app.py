from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import OpenAI (optional)
try:
    from openai import OpenAI
    # Initialize OpenAI client
    openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY')) if os.getenv('OPENAI_API_KEY') else None
    OPENAI_AVAILABLE = True
except ImportError:
    print("⚠️  OpenAI package not installed. Using fallback responses only.")
    openai_client = None
    OPENAI_AVAILABLE = False

# Fashion specialist system prompt
FASHION_SYSTEM_PROMPT = """
You are an expert AI Fashion Specialist with extensive knowledge in:
- Outfit coordination and styling for all occasions
- Makeup techniques and beauty advice
- Hair styling and care
- Jewelry and accessories coordination
- Color theory and matching
- Body type specific styling
- Seasonal fashion trends
- Footwear selection
- Fashion for different age groups and lifestyles

Provide detailed, practical, and personalized fashion advice. Always give multiple options and explain your reasoning. Be encouraging and help boost confidence. Format your responses clearly with sections for different aspects (outfits, accessories, makeup, etc.) when relevant.
"""

class FashionAssistant:
    def __init__(self):
        self.conversation_history = {}
    
    def get_fashion_advice(self, message, chat_history=None, user_id="default"):
        """
        Generate fashion advice using AI or fallback responses
        """
        try:
            # Try AI response first if available
            if openai_client and OPENAI_AVAILABLE:
                return self.get_ai_response(message, chat_history)
            else:
                return self.get_fallback_response(message)
                
        except Exception as e:
            logger.error(f"Error generating fashion advice: {str(e)}")
            return self.get_fallback_response(message)
    
    def get_ai_response(self, message, chat_history=None):
        """
        Get AI-powered fashion advice using OpenAI
        """
        try:
            # Prepare conversation context
            messages = [{"role": "system", "content": FASHION_SYSTEM_PROMPT}]
            
            # Add chat history if provided
            if chat_history:
                for chat in chat_history[-10:]:  # Keep last 10 messages for context
                    messages.append({
                        "role": chat.get("role", "user"),
                        "content": chat.get("content", "")
                    })
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Get response from OpenAI
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return self.get_fallback_response(message)
    
    def get_fallback_response(self, message):
        """
        Comprehensive fallback fashion responses when AI is not available
        """
        message_lower = message.lower()
        
        # Work/Interview styling
        if any(word in message_lower for word in ['work', 'interview', 'office', 'professional', 'business']):
            return """💼 **Professional Styling Advice:**

**Outfit Options:**
1. Classic navy blazer with tailored trousers and crisp white shirt
2. Sheath dress in black or navy with structured jacket
3. Button-down shirt with pencil skirt and closed-toe heels
4. Professional pantsuit in neutral colors (navy, charcoal, black)

**Footwear:**
• Closed-toe pumps with 2-3 inch heel
• Oxford shoes for a modern touch
• Low block heels for comfort
• Professional loafers

**Accessories:**
• Simple watch (leather or metal band)
• Minimal jewelry (stud earrings, simple necklace)
• Structured handbag or briefcase
• Classic leather belt

**Makeup:**
• Natural, polished look
• Neutral eyeshadow palette
• Professional lipstick (nude, berry, or classic red)
• Well-groomed eyebrows

**Pro Tips:** Keep it conservative, ensure perfect fit, and remember - you want to be remembered for your skills, not your outfit!"""
        
        # Casual styling
        elif any(word in message_lower for word in ['casual', 'weekend', 'relaxed', 'everyday']):
            return """😎 **Casual Styling Guide:**

**Outfit Ideas:**
1. High-waisted jeans with cozy sweater and white sneakers
2. Midi dress with denim jacket and ankle boots
3. Casual blazer with jeans and basic tee
4. Comfortable joggers with stylish hoodie and sneakers

**Footwear:**
• White leather sneakers (versatile and trendy)
• Ankle boots for added style
• Slip-on shoes for easy wear
• Canvas shoes for summer

**Accessories:**
• Crossbody bag for hands-free convenience
• Baseball cap or beanie
• Layered necklaces
• Casual watch or fitness tracker

**Makeup:**
• Fresh, natural look
• Tinted moisturizer instead of foundation
• Lip balm or tinted lip gloss
• Just mascara for defined eyes

**Style Tips:** Comfort is key! Mix textures, don't be afraid of patterns, and remember casual doesn't mean sloppy!"""
        
        # Wedding/Formal events
        elif any(word in message_lower for word in ['wedding', 'formal', 'ceremony', 'special event']):
            return """💒 **Wedding & Special Event Styling:**

**Outfit Options:**
1. Elegant midi dress in pastels (avoid white/ivory/cream)
2. Sophisticated jumpsuit with heels
3. Floral dress with cardigan for outdoor weddings
4. Classic A-line dress with modest neckline

**Footwear:**
• Block heels for stability
• Wedges for outdoor/garden weddings
• Elegant flats if you'll be standing long
• Strappy sandals for evening events

**Accessories:**
• Statement earrings
• Small clutch purse
• Delicate bracelet
• Hair accessories (if appropriate)

**Makeup:**
• Romantic, soft glam look
• Rosy cheeks for a healthy glow
• Neutral to pink lips
• Defined but not dramatic eyes

**Event Tips:** Consider the venue (indoor/outdoor), bring a wrap for air conditioning, and choose shoes you can dance in!"""
        
        # Party/Evening
        elif any(word in message_lower for word in ['party', 'evening', 'night out', 'date', 'club']):
            return """🎉 **Party & Evening Styling:**

**Outfit Ideas:**
1. Little black dress with statement accessories
2. Sequined or metallic top with black trousers
3. Silk camisole with high-waisted pants
4. Bodycon dress with blazer for sophistication

**Footwear:**
• High heels for glamour
• Strappy sandals
• Pointed-toe pumps
• Stylish ankle boots

**Accessories:**
• Bold jewelry (statement necklace or earrings)
• Evening clutch
• Statement belt to define waist
• Elegant scarf or wrap

**Makeup:**
• Bold smoky eyes or dramatic lashes
• Red or berry lips for impact
• Highlighted cheekbones
• Don't forget setting spray!

**Party Tips:** This is your time to shine! Don't be afraid of bold choices, but ensure you can move comfortably."""
        
        # Hair styling
        elif any(word in message_lower for word in ['hair', 'hairstyle', 'haircut']):
            return """💇‍♀️ **Hair Styling Guide:**

**For Long Hair:**
• Beach waves for effortless elegance
• Sleek straight hair for professional look
• High ponytail for active days
• Braided crown for special occasions

**For Medium Hair:**
• Lob (long bob) with subtle layers
• Textured bob for modern style
• Half-up half-down for versatility
• Side-swept bangs for face framing

**For Short Hair:**
• Pixie cut with texturizing products
• Textured crop for edgy look
• Side-swept styling
• Add headbands or clips for variety

**For Curly Hair:**
• Define curls with leave-in cream
• Twist-outs for stretched curls
• Protective styles for hair health
• Embrace your natural texture!

**Pro Tips:** Always use heat protectant, consider your face shape, get regular trims, and don't fight your natural texture!"""
        
        # Makeup
        elif any(word in message_lower for word in ['makeup', 'beauty', 'cosmetics']):
            return """💄 **Makeup & Beauty Guide:**

**Everyday Makeup:**
• Tinted moisturizer or light foundation
• Concealer for under eyes and blemishes
• Cream blush for natural flush
• Mascara and lip balm

**Work Makeup:**
• Medium coverage foundation
• Neutral eyeshadow palette
• Defined brows
• Professional lipstick

**Evening Makeup:**
• Full coverage foundation
• Smoky eyes or bold lips (not both)
• Contouring and highlighting
• Setting spray for longevity

**Makeup Tips:**
• Match foundation to your neck, not your hand
• Blend eyeshadow upward and outward
• Use lip liner to make lipstick last longer
• Clean brushes regularly for better application

**Skincare First:** Always start with clean, moisturized skin for best makeup application!"""
        
        # Color coordination
        elif any(word in message_lower for word in ['color', 'colour', 'match', 'coordinate']):
            return """🎨 **Color Coordination Guide:**

**Color Combinations:**
• **Complementary:** Blue & Orange, Red & Green, Purple & Yellow
• **Analogous:** Colors next to each other on color wheel
• **Monochromatic:** Different shades of same color
• **Neutral Base:** Black, white, beige, navy - pair with any accent color

**Skin Tone Tips:**
• **Cool Undertones:** Jewel tones (emerald, sapphire, ruby)
• **Warm Undertones:** Earth tones (rust, gold, olive)
• **Neutral Undertones:** Most colors work well

**Quick Rules:**
• When in doubt, add one pop of color to neutrals
• Limit yourself to 3 colors maximum
• Use the 60-30-10 rule: 60% dominant color, 30% secondary, 10% accent

**Safe Combinations:**
• Navy + white + gold accents
• Black + cream + one bright color
• Beige + brown + metallics"""
        
        # Default response
        else:
            return """✨ **Welcome to Your Fashion Consultation!**

I'm here to help you with all aspects of fashion and style! I can assist you with:

👗 **Styling Services:**
• Complete outfit coordination
• Occasion-specific dressing
• Color matching and coordination
• Body type specific advice

💄 **Beauty & Hair:**
• Makeup tutorials and tips
• Hairstyle recommendations
• Skincare advice
• Beauty product suggestions

💎 **Accessories:**
• Jewelry coordination
• Bag and shoe pairing
• Seasonal accessories
• Investment piece advice

**What would you like help with today?** You can ask me about:
- Outfits for specific occasions
- Hair styling ideas
- Makeup looks
- Color coordination
- Accessory advice
- Or any other fashion question!

I'm here to help you look and feel your best! 💫"""

# Initialize fashion assistant
fashion_assistant = FashionAssistant()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'AI Fashion Specialist',
        'ai_enabled': openai_client is not None
    })

@app.route('/api/fashion-chat', methods=['POST'])
def fashion_chat():
    """Main chat endpoint for fashion advice"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message']
        chat_history = data.get('chatHistory', [])
        user_id = data.get('userId', 'default')
        
        logger.info(f"Received fashion query: {message[:50]}...")
        
        # Get fashion advice
        response = fashion_assistant.get_fashion_advice(
            message=message,
            chat_history=chat_history,
            user_id=user_id
        )
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error in fashion chat: {str(e)}")
        return jsonify({
            'error': 'Sorry, I encountered an error. Please try again.',
            'timestamp': datetime.now().isoformat(),
            'status': 'error'
        }), 500

@app.route('/')
def serve_frontend():
    """Serve basic info page"""
    ai_status = "✅ AI-Powered" if openai_client else "⚠️ Fallback Mode"
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Fashion Specialist Backend</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ background: white; padding: 30px; border-radius: 10px; max-width: 600px; }}
            .status {{ padding: 10px; border-radius: 5px; margin: 10px 0; }}
            .success {{ background: #d4edda; color: #155724; }}
            .warning {{ background: #fff3cd; color: #856404; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 AI Fashion Specialist Backend</h1>
            <div class="status {'success' if openai_client else 'warning'}">
                Status: {ai_status}
            </div>
            <p>Backend is running successfully! Use your HTML frontend to interact with the fashion assistant.</p>
            
            <h3>📡 API Endpoints:</h3>
            <ul>
                <li><strong>GET /api/health</strong> - Health check</li>
                <li><strong>POST /api/fashion-chat</strong> - Fashion advice chat</li>
            </ul>
            
            <h3>💡 Setup Instructions:</h3>
            <ol>
                <li>Update your HTML frontend baseURL to: <code>http://localhost:3000/api</code></li>
                <li>Optional: Set OPENAI_API_KEY environment variable for AI responses</li>
                <li>Start chatting with your fashion assistant!</li>
            </ol>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    # Configuration
    port = int(os.environ.get('PORT', 3000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print("🚀 Starting AI Fashion Specialist Backend...")
    print(f"📡 Server will run on http://localhost:{port}")
    print("💡 Make sure to update the frontend baseURL to match this address")
    
    if openai_client:
        print("✅ OpenAI API key found - Using GPT for intelligent responses")
    else:
        print("⚠️  No OpenAI API key found - Using comprehensive fallback responses")
        print("   Set OPENAI_API_KEY environment variable for AI-powered responses")
    
    app.run(host='0.0.0.0', port=port, debug=debug)