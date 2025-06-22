To run flask_app.py manually, you can follow these steps:
1. Open https://developers.kite.trade/ signup/signin and create an app with following details:
   - App Name: `kiteAPI`
   - Redirect URL: `http://localhost:9899/login`
2. install required dependencies:
   pip3 install kiteconnect dotenv flask
3. Create a `.env` file in the home directory with this:
   ```
   KITE_API_KEY=your_api_key
   KITE_API_SECRET=your_api_secret
   ```
4. Run the app:
   ```
   python3.11 examples/flask_app.py
   ```
5. open http://127.0.0.1:5010/ and click on "Login to generate access token" it will redirect you to the actual page.
   you can explore the holdings and orders from there.