# 🚀 Vercel + Supabase Deployment Checklist

## ✅ Pre-Deployment Setup

### 1. Generate Secret Key
```bash
python generate_secret_key.py
```
- Copy the generated SECRET_KEY

### 2. Test Supabase Connection
```bash
python test_supabase_connection.py
```
- Enter your Supabase database password
- Verify connection is successful

### 3. Set Up Database
```bash
python setup_supabase_database.py
```
- Run Django migrations
- Create superuser if needed

## ✅ Vercel Environment Variables

Add these to your Vercel project settings:

### Database Configuration
- `DB_HOST` = `db.ydexeftnucyjnorycrpd.supabase.co`
- `DB_NAME` = `postgres`
- `DB_USER` = `postgres`
- `DB_PASSWORD` = `[Your Supabase password]`
- `DB_PORT` = `5432`

### Django Configuration
- `SECRET_KEY` = `[Generated secret key]`
- `DEBUG` = `False`
- `GOOGLE_MAPS_API_KEY` = `AIzaSyAvP5QtAlj_WcbZ84Yoo2K_I_MGW8guO30`

### Supabase Configuration
- `SUPABASE_URL` = `https://ydexeftnucyjnorycrpd.supabase.co`
- `SUPABASE_ANON_KEY` = `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlkZXhlZnRudWN5am5vcnljcnBkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk0OTM0NDUsImV4cCI6MjA3NTA2OTQ0NX0.QpzB4MN-7WIhjSSLyR8x9Mguj904HpI40AgokU-RhLE`

## ✅ Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Add Supabase configuration and migration scripts"
git push origin main
```

### 2. Deploy on Vercel
- Go to vercel.com
- Import your GitHub repository
- Set all environment variables
- Deploy

### 3. Run Migrations on Vercel
Visit: `https://your-vercel-url.vercel.app/api/migrate`

## ✅ Testing Checklist

### 1. Basic Functionality
- [ ] Homepage loads
- [ ] User registration works
- [ ] User login works
- [ ] Routes display correctly
- [ ] Booking creation works
- [ ] QR code generation works

### 2. Database Connection
- [ ] Check Supabase dashboard for tables
- [ ] Verify data is being saved
- [ ] Test admin panel access

### 3. Static Files
- [ ] CSS loads correctly
- [ ] Images display properly
- [ ] JavaScript functions work

## 🔧 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check environment variables
   - Verify Supabase project is active
   - Test connection locally first

2. **Static Files Not Loading**
   - Check WhiteNoise configuration
   - Verify STATIC_ROOT setting

3. **Migrations Failed**
   - Check database permissions
   - Verify connection string
   - Run migrations locally first

### Support Resources
- Vercel Documentation: https://vercel.com/docs
- Supabase Documentation: https://supabase.com/docs
- Django Deployment Guide: https://docs.djangoproject.com/en/stable/howto/deployment/

## 🎉 Success!

Once everything is working:
1. Your Django app is deployed on Vercel
2. Connected to Supabase PostgreSQL database
3. Static files are served correctly
4. All functionality is working

Your bus booking system is now live! 🚌✨
