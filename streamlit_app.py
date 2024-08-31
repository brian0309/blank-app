from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def license_check(product_link, license_key, api_key):
    url = f"https://payhip.com/api/v1/license/verify?product_link={product_link}&license_key={license_key}"
    headers = {"payhip-api-key": api_key}
    response = requests.get(url, headers=headers)
    result = response.json()
    try:
        enabled = result['data']['enabled']
    except:
        enabled = False
    success = result.get('success', False)
    message = result.get('message', 'Please contact the seller, input the correct key or redownload the application.')
    return success, message, enabled

def check(product_link, license_key, api_key):
    success, message, enabled = license_check(product_link, license_key, api_key)
    if not success:
        result = False
        if message == "failed to authenticate":
            print("Cannot verify the license. Msg: Auth-failed. \nPlease redownload the latest version. Same download link from the purchase email. Thank you.")
        else:
            if enabled:
                print("License verified.")
                result = True
            else:
                print(f"Verification failed. {message}")
    else: 
        result = True
        print("License Verified.")
    return result

@app.route('/check_license', methods=['POST'])
def check_license():
    data = request.json
    product_link = data.get('product_link')
    license_key = data.get('license_key')
    api_key = data.get('api_key')

    if not product_link or not license_key or not api_key:
        return jsonify({"error": "Missing required parameters"}), 400

    result = check(product_link, license_key, api_key)
    return jsonify({"valid": result})

if __name__ == '__main__':
    app.run(debug=True)