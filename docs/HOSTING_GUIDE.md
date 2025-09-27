# Hosting Guide for Baseball Lineup App

## **Recommended: Heroku (Best for Getting Started)**

### **Why Heroku:**
- **Simplest deployment** - git push to deploy
- **Built-in PostgreSQL** - managed database included
- **SSL certificates** - automatic HTTPS
- **Add-ons ecosystem** - Redis, monitoring, etc.
- **Stripe-friendly** - webhooks work seamlessly

### **Heroku Pricing:**
```
Hobby Plan: $7/month
- 1 web dyno, 1 worker dyno
- 10,000 database rows
- Custom domain, SSL
- Good for 100-500 users

Standard Plan: $25/month  
- More database storage
- Better performance
- Good for 500-2000 users
```

### **Heroku Deployment Steps:**
1. Create Heroku account
2. Install Heroku CLI
3. `git push heroku main` - app goes live
4. Add PostgreSQL add-on
5. Set environment variables in Heroku dashboard

---

## **Alternative: DigitalOcean App Platform**

### **Why DigitalOcean:**
- **Good value** - $5-12/month for basic apps
- **Managed platform** - like Heroku but cheaper
- **Built-in databases** - PostgreSQL included
- **Simple scaling** - easy to upgrade

### **DigitalOcean Pricing:**
```
Basic: $5/month
- 1 GB RAM, good for small user base

Pro: $12/month  
- 2 GB RAM, better for growth
```

---

## **For Larger Scale: AWS/Google Cloud**

### **When to Consider:**
- 1000+ users
- Need advanced features (auto-scaling, CDN)
- Want maximum control

### **AWS Services Needed:**
- **Elastic Beanstalk** - app hosting
- **RDS PostgreSQL** - managed database  
- **Route 53** - domain management
- **CloudFront** - CDN for static files

### **Pricing (AWS):**
```
Small Setup: $30-50/month
- t3.micro instances
- RDS db.t3.micro
- Minimal traffic

Medium Setup: $100-200/month
- Better instances
- Multi-AZ database
- Higher traffic capacity
```

---

## **Budget Option: Railway**

### **Why Railway:**
- **Very cheap** - $5/month starts
- **Simple deployment** - connect GitHub repo
- **Built-in PostgreSQL**
- **Good for MVP testing**

---

## **Hosting Comparison:**

| Provider | Monthly Cost | Complexity | Best For |
|----------|-------------|------------|----------|
| **Heroku** | $7-25 | Low | Getting started quickly |
| **DigitalOcean** | $5-12 | Low | Cost-conscious with growth |
| **Railway** | $5-15 | Very Low | MVP testing |
| **AWS** | $30-200+ | High | Large scale, enterprise |
| **Vercel** | $0-20 | Low | Frontend-heavy apps |

---

## **Recommended Path: Start with Heroku**

### **Phase 1: MVP (Heroku Hobby - $7/month)**
- Deploy current app
- Add 10-20 beta users
- Test payment integration
- Validate product-market fit

### **Phase 2: Growth (Heroku Standard - $25/month)**  
- 100-500 paying users
- Add monitoring, caching
- Scale database

### **Phase 3: Scale (Consider AWS - $50-200/month)**
- 1000+ users
- Need advanced features
- Custom infrastructure requirements

---

## **Additional Services You'll Need:**

### **Domain & Email:**
- **Domain**: Namecheap, Google Domains ($10-15/year)
- **Email**: Google Workspace ($6/user/month) or SendGrid for transactional emails

### **Monitoring & Analytics:**
- **Error Tracking**: Sentry (free tier, then $26/month)
- **Analytics**: Google Analytics (free) or Mixpanel
- **Uptime Monitoring**: Pingdom ($10/month) or UptimeRobot (free)

### **CDN (for better performance):**
- **Cloudflare**: Free tier with basic CDN
- **AWS CloudFront**: Pay-per-use

---

## **Total Monthly Costs by Phase:**

### **MVP Phase:**
```
Heroku Hobby: $7
Domain: $1 (annual/12)
Total: ~$8/month
```

### **Growth Phase:**
```
Heroku Standard: $25
Sentry: $26
Domain: $1
SendGrid: $15
Total: ~$67/month
```

### **Scale Phase:**
```
AWS Infrastructure: $100-200
Additional services: $50
Total: $150-250/month
```

---

## **Deployment Strategy:**

### **Week 1: Heroku Setup**
1. Create Heroku account
2. Deploy current app to Heroku
3. Set up custom domain
4. Test with 2-3 users

### **Week 2: Payment Integration**
1. Add Stripe to Heroku app
2. Set up webhook endpoints
3. Test subscription flow

### **Week 3: Beta Launch**
1. Invite 10-20 beta users
2. Monitor performance
3. Gather feedback

### **Month 2-3: Optimize**
1. Add monitoring/analytics
2. Optimize based on usage patterns
3. Plan scaling strategy

---

## **Quick Start: Heroku Deployment**

```bash
# Install Heroku CLI
npm install -g heroku

# Login and create app
heroku login
heroku create your-lineup-app

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set TEAMSNAP_CLIENT_ID=your_id
heroku config:set TEAMSNAP_CLIENT_SECRET=your_secret
heroku config:set STRIPE_SECRET_KEY=your_stripe_key

# Deploy
git push heroku main

# Your app is live at: https://your-lineup-app.herokuapp.com
```

**Bottom Line**: Start with Heroku for simplicity and speed. You can always migrate to other platforms later as you grow. The key is getting your MVP live quickly to validate demand before investing in complex infrastructure.