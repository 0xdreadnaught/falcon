# falcon
AIO web reconnaissance tool

Supported Platforms: Linux / Windows (Bash enabled)

Features:
- CDN detection 
- CMS detection
- Banner grabbing
- Whois lookup (incomplete)
- Web crawling (incomplete)
- more to come

Feature Breakdown:

CDN DETECTION:
Currently supports detection of the following CDN platforms:
- CloudFlare
- Incapsula
- KeyCDN
- Akamai
- CloudFront
- CacheFly
- EdgeCast
- BitGravity
- Fastly
- FireBlade
- MaxCDN
- Netlify

CMS DETECTION:
Currently supports detection of CMS platforms via path validation and HTML based signatures:
- WordPress
- Joomla!
- Drupal
- SquareSpace
- Weebly
- Typo3 CMS
- Jimdo
- DNN
- SharePoint

BANNER GRABBING:
Utilizes Curl -I <URL> to grab target banner information

Currently Working On:
CMS Detection: Need  to implement a more indepth method for validating /mis/drupal.js as well as scrubbing invalid url for sharepoint errors

