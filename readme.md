## Intro

> support by chatgpt, code by python(flask) html, css, javascript

**./**

using flask & js & html to generate a simple login page and jwt authentication service.

login page support dark and light theme, like below:

![dark](https://picture-bed-001-1310572365.cos.ap-guangzhou.myqcloud.com/3070PC/20240118232124.png)

![light](https://picture-bed-001-1310572365.cos.ap-guangzhou.myqcloud.com/3070PC/20240118232221.png)

when u input wrong password, cat(ron) will comes up to tell you wrong credentials.

![cat](https://picture-bed-001-1310572365.cos.ap-guangzhou.myqcloud.com/3070PC/20240118232314.png)

**/nginx_template**

Use the auth_request feature of Nginx to implement unified authentication for various services. Now assume that your service is deployed on port 2323, and the authentication port is 2424.

Remember to replace the {your_.*} in there with your own address, domain, and port respectively.

## FI
