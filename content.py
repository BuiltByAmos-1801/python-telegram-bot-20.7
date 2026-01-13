# Content data
AI_PROMPTS = [
   """🔹 PREMIUM AI PROMPT PACKAGE (2026 TREND)
1️⃣ YouTube / Shorts Script Generator

Prompt:

You are an expert content creator. Generate a 40-second YouTube Shorts script for [topic]. The script should be engaging, hook in the first 5 seconds, include 3 key points, and a strong call to action. Output in bullet points suitable for narration.

2️⃣ Blog / Article Generator

Prompt:

You are an AI writing assistant. Write a professional 500-word blog article on [topic]. Include introduction, subheadings, examples, and a conclusion with a call to action. Use easy-to-read language suitable for beginners.

3️⃣ Social Media Caption Creator

Prompt:

You are a creative social media expert. Generate 5 catchy Instagram/TikTok captions for [topic]. Each caption should be under 100 characters, include trending hashtags, and be highly engaging.

4️⃣ Affiliate / Online Earning Post Generator

Prompt:

You are an expert in online earning. Create 3 short posts for Telegram or Instagram promoting [product/earning method]. Each post must include key benefits, earning potential, and a call to action. Tone: friendly + motivational.

5️⃣ AI Image Prompt Creator

Prompt:

You are a professional AI image prompt writer. Generate 3 highly detailed prompts for MidJourney/DALL·E to create [topic] images. Include style, color, lighting, and mood details.

6️⃣ Mini Course / Guide Outline Generator

Prompt:

You are an expert teacher. Create a step-by-step 5-chapter mini-course outline on [topic]. Include lesson titles, key points, practical tasks for users, and estimated completion time for each chapter.

7️⃣ Telegram Bot Engagement Prompt

Prompt:

You are a Telegram bot engagement expert. Suggest 5 daily messages or tips that can be sent to paid users about [topic]. Each message should be short, actionable, and increase retention."""
]

EARNING_GUIDES = [
    """💸 PREMIUM EARNING GUIDES (2026 TRENDING)
1️⃣ Freelancing Fast-Track (₹0–₹10,000/month start)

Platforms: Fiverr, Upwork, Freelancer

Skills: Content writing, graphic design, video editing, AI prompt writing

Step-by-step:

Account setup + portfolio

Profile optimization

First 3 gigs setup

Client outreach template (ready)

Bonus tip: AI tools to speed up work → Canva AI, ChatGPT, MidJourney

2️⃣ AI-Powered Micro Jobs

Websites: Clickworker, Remotasks, Appen, Amazon MTurk

How to earn: AI-assisted data labeling, transcription, micro surveys

Daily earning potential: ₹500–₹2,000

Guide includes:

Step-by-step registration

Best-paying tasks

Time management tips

3️⃣ Online Course + Digital Product Sale

Platforms: Gumroad, Ko-fi, Shopify Lite

Product ideas:

AI prompts bundle

Mini earning guides

Templates / scripts

Steps:

Product creation (PDF / template)

Hosting on free platform

Telegram bot integration for paid access

4️⃣ YouTube Shorts / Reels Monetization

Create niche: AI tutorials, online earning tips, productivity hacks

Monetization methods:

YouTube Shorts Fund

Affiliate links in description

Channel sponsorships (small brands)

Guide includes:

Video creation workflow (phone-friendly)

Caption + script templates

Posting schedule (daily / weekly)

5️⃣ Affiliate Marketing – Mobile Friendly

Platforms: Amazon, Flipkart, Hosting affiliates, AI tools

Step-by-step:

Niche selection

Telegram / social media promotion

Link shortening + tracking

Bonus: Bot can send exclusive affiliate tips / links

6️⃣ ChatGPT / AI Tool Subscription Reselling

Buy AI tool access (paid plans)

Sell micro-access / tips via Telegram bot

Steps:

License / subscription purchase

Paid access bot setup (manual verify)

Send guides + tutorials inside bot

Note: Keep legal + terms in mind"""
]

TUTORIALS = [
    """🎓 PREMIUM TUTORIALS IDEAS FOR BOT
1️⃣ AI & Automation Tutorials (High Demand)

ChatGPT Mastery

Prompt engineering step-by-step

AI content creation for blogs, YouTube, social media

Example: “How to generate 10 YouTube scripts in 5 minutes”

AI Image/Video Tools

MidJourney, DALL·E, Runway AI

Step-by-step guides on creating digital art / thumbnails / video clips

Automation with Python / Scripts

Telegram bot creation basics

Task automation (sending content, reminders)

Example: Auto posting AI prompts

2️⃣ Online Earning Tutorials (Step-By-Step)

Freelancing Crash Course

Fiverr / Upwork account setup + profile optimization

Gig creation + portfolio examples

Tips for first 5 paid orders

Affiliate Marketing for Beginners

Niche selection + affiliate link creation

Telegram / social media promotion

Tracking + commission collection

Digital Product Selling

Mini e-books, PDF guides, templates

Hosting (Gumroad / Ko-fi / Google Drive + Telegram bot integration)

Pricing + marketing strategies

3️⃣ YouTube / Shorts Tutorials

AI + Tools for Shorts

Creating 30–60 second viral videos using AI

Script writing, thumbnail creation, caption ideas

Monetization

YouTube Shorts Fund, affiliate links, sponsorships

Batch Production Tips

Create 5–10 shorts in 1 hour using AI tools

4️⃣ Productivity & Tech Tutorials

Mobile-Only Workflows

Creating content / earning using just phone

Apps for design, scheduling, video editing

Telegram Bot Hacks

Simple commands, broadcasting tips, paid content management

AI-Powered Research

How to collect data / market trends using AI tools

Step-by-step scraping / auto summary using ChatGPT

5️⃣ Bonus / Premium Tutorials

Portfolio Building

How to create a strong online portfolio (Fiverr / LinkedIn / Behance)

Mini Case Studies

Real earning examples, step-by-step method used

Growth & Marketing

Telegram channel growth hacks

Social media cross promotion for paid guides"""
]

PRIVATE_CHANNEL = "https://t.me/ConnectServiceHubAmos180704"  

def get_daily_content(day):
    """Get daily content based on day"""
    index = day % len(AI_PROMPTS)
    return {
        'ai_prompt': AI_PROMPTS[index],
        'earning_guide': EARNING_GUIDES[index % len(EARNING_GUIDES)],
        'tutorial': TUTORIALS[index % len(TUTORIALS)]
    }