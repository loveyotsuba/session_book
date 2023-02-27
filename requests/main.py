import requests

param = {'name': 'test3', 'password': '123456', 'phone': 'phone3'}
url = 'http://localhost:8000/'

cookie_value = {'token': '2|1:0|10:1677224721|5:token|304:ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6STFOaUo5LmV5SmtZWFJoSWpwN0ltNWhiV1VpT2lKMFpYTjBNeUlzSW14dloybHVYM1JwYldVaU9pSXlNREl6TFRBeUxUSTBJREUxT2pRMU9qSXhJbjBzSW1WNGNDSTZNVFkzT1RnME5UVXlNU3dpYVhOemRXVmZkR2x0WlNJNklqRTFMVEF5TFRJMElERTFPalExT2pJeEluMC44YThjZ3RZNUtRaFk0YVRRV2VJU3czcEJ4cjFUN0o2UHE4VjJDcEppSGNJ|16a3e2b464773fa2c79631ef7d0f5ebd60da3f8c004c9068ca2d24350473ee99'}

res = requests.get(url, params=param, cookies=cookie_value)
print(res, res.text)
