var dateFormat = function () {
    var token = /d{1,4}|m{1,4}|yy(?:yy)?|([HhMsTt])\1?|[LloSZWN]|'[^']*'|'[^']*'/g;
    var timezone = /\b(?:[PMCEA][SDP]T|(?:Pacific|Mountain|Central|Eastern|Atlantic) (?:Standard|Daylight|Prevailing) Time|(?:GMT|UTC)(?:[-+]\d{4})?)\b/g;
    var timezoneClip = /[^-+\dA-Z]/g;

    // Regexes and supporting functions are cached through closure
    return function (date, mask, utc, gmt) {

        // You can't provide utc if you skip other args (use the 'UTC:' mask prefix)
        if (arguments.length === 1 && kindOf(date) === 'string' && !/\d/.test(date)) {
            mask = date;
            date = undefined;
        }

        date = date || new Date();

        if (!(date instanceof Date)) {
            date = new Date(date);
        }

        if (isNaN(date)) {
            throw TypeError('Invalid date');
        }

        mask = String(dateFormat.masks[mask] || mask || dateFormat.masks['default']);

        // Allow setting the utc/gmt argument via the mask
        var maskSlice = mask.slice(0, 4);
        if (maskSlice === 'UTC:' || maskSlice === 'GMT:') {
            mask = mask.slice(4);
            utc = true;
            if (maskSlice === 'GMT:') {
                gmt = true;
            }
        }

        var _ = utc ? 'getUTC' : 'get';
        var d = date[_ + 'Date']();
        var D = date[_ + 'Day']();
        var m = date[_ + 'Month']();
        var y = date[_ + 'FullYear']();
        var H = date[_ + 'Hours']();
        var M = date[_ + 'Minutes']();
        var s = date[_ + 'Seconds']();
        var L = date[_ + 'Milliseconds']();
        var o = utc ? 0 : date.getTimezoneOffset();
        var W = getWeek(date);
        var N = getDayOfWeek(date);
        var flags = {
            d: d,
            dd: pad(d),
            ddd: dateFormat.i18n.dayNames[D],
            dddd: dateFormat.i18n.dayNames[D + 7],
            m: m + 1,
            mm: pad(m + 1),
            mmm: dateFormat.i18n.monthNames[m],
            mmmm: dateFormat.i18n.monthNames[m + 12],
            yy: String(y).slice(2),
            yyyy: y,
            h: H % 12 || 12,
            hh: pad(H % 12 || 12),
            H: H,
            HH: pad(H),
            M: M,
            MM: pad(M),
            s: s,
            ss: pad(s),
            l: pad(L, 3),
            L: pad(Math.round(L / 10)),
            t: H < 12 ? 'a' : 'p',
            tt: H < 12 ? 'am' : 'pm',
            T: H < 12 ? 'A' : 'P',
            TT: H < 12 ? 'AM' : 'PM',
            Z: gmt ? 'GMT' : utc ? 'UTC' : (String(date).match(timezone) || ['']).pop().replace(timezoneClip, ''),
            o: (o > 0 ? '-' : '+') + pad(Math.floor(Math.abs(o) / 60) * 100 + Math.abs(o) % 60, 4),
            S: ['th', 'st', 'nd', 'rd'][d % 10 > 3 ? 0 : (d % 100 - d % 10 != 10) * d % 10],
            W: W,
            N: N
        };

        return mask.replace(token, function (match) {
            if (match in flags) {
                return flags[match];
            }
            return match.slice(1, match.length - 1);
        });
    };
}()

dateFormat.masks = {
    'default': 'ddd mmm dd yyyy HH:MM:ss',
    'shortDate': 'm/d/yy',
    'mediumDate': 'mmm d, yyyy',
    'longDate': 'mmmm d, yyyy',
    'fullDate': 'dddd, mmmm d, yyyy',
    'shortTime': 'h:MM TT',
    'mediumTime': 'h:MM:ss TT',
    'longTime': 'h:MM:ss TT Z',
    'isoDate': 'yyyy-mm-dd',
    'isoTime': 'HH:MM:ss',
    'isoDateTime': 'yyyy-mm-dd\'T\'HH:MM:sso',
    'isoUtcDateTime': 'UTC:yyyy-mm-dd\'T\'HH:MM:ss\'Z\'',
    'expiresHeaderFormat': 'ddd, dd mmm yyyy HH:MM:ss Z'
};
dateFormat.i18n = {
    dayNames: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
    monthNames: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
};

function pad(val, len) {
    val = String(val);
    len = len || 2;
    while (val.length < len) {
        val = '0' + val;
    }
    return val;
}

/**
 * Get the ISO 8601 week number
 * Based on comments from
 * http://techblog.procurios.nl/k/n618/news/view/33796/14863/Calculate-ISO-8601-week-and-year-in-javascript.html
 *
 * @param  {Object} `date`
 * @return {Number}
 */
function getWeek(date) {
    // Remove time components of date
    var targetThursday = new Date(date.getFullYear(), date.getMonth(), date.getDate());

    // Change date to Thursday same week
    targetThursday.setDate(targetThursday.getDate() - (targetThursday.getDay() + 6) % 7 + 3);

    // Take January 4th as it is always in week 1 (see ISO 8601)
    var firstThursday = new Date(targetThursday.getFullYear(), 0, 4);

    // Change date to Thursday same week
    firstThursday.setDate(firstThursday.getDate() - (firstThursday.getDay() + 6) % 7 + 3);

    // Check if daylight-saving-time-switch occurred and correct for it
    var ds = targetThursday.getTimezoneOffset() - firstThursday.getTimezoneOffset();
    targetThursday.setHours(targetThursday.getHours() - ds);

    // Number of weeks between target Thursday and first Thursday
    var weekDiff = (targetThursday - firstThursday) / (86400000 * 7);
    return 1 + Math.floor(weekDiff);
}

/**
 * Get ISO-8601 numeric representation of the day of the week
 * 1 (for Monday) through 7 (for Sunday)
 * 
 * @param  {Object} `date`
 * @return {Number}
 */
function getDayOfWeek(date) {
    var dow = date.getDay();
    if (dow === 0) {
        dow = 7;
    }
    return dow;
}


function _interopRequireDefault(obj) {
    return obj && obj.__esModule ? obj : {
        default: obj
    };
}

var _keys = require('babel-runtime/core-js/object/keys');
var _keys2 = _interopRequireDefault(_keys);

var is = require('is-type-of');
// var crypto = require('./../../shims/crypto/crypto.js');
var crypto = require('crypto')

function buildCanonicalizedResource(resourcePath, parameters) {
    var canonicalizedResource = '' + resourcePath;
    var separatorString = '?';

    if (is.string(parameters) && parameters.trim() !== '') {
        canonicalizedResource += separatorString + parameters;
    } else if (is.array(parameters)) {
        parameters.sort();
        canonicalizedResource += separatorString + parameters.join('&');
    } else if (parameters) {
        var compareFunc = function compareFunc(entry1, entry2) {
            if (entry1[0] > entry2[0]) {
                return 1;
            } else if (entry1[0] < entry2[0]) {
                return -1;
            }
            return 0;
        };
        var processFunc = function processFunc(key) {
            canonicalizedResource += separatorString + key;
            if (parameters[key]) {
                canonicalizedResource += '=' + parameters[key];
            }
            separatorString = '&';
        };
        (0, _keys2.default)(parameters).sort(compareFunc).forEach(processFunc);
    }

    return canonicalizedResource;
}

function canonicalString(method, resourcePath, request, expires) {
    request = request || {};
    var headers = request.headers || {};
    var OSS_PREFIX = 'x-oss-';
    var ossHeaders = [];
    var headersToSign = {};

    var signContent = [method.toUpperCase(), headers['Content-Md5'] || '', headers['Content-Type'] || headers['Content-Type'.toLowerCase()], expires || headers['x-oss-date']];


    (0, _keys2.default)(headers).forEach(function (key) {
        var lowerKey = key.toLowerCase();
        if (lowerKey.indexOf(OSS_PREFIX) === 0) {
            headersToSign[lowerKey] = String(headers[key]).trim();
        }
    });

    (0, _keys2.default)(headersToSign).sort().forEach(function (key) {
        ossHeaders.push(key + ':' + headersToSign[key]);
    });

    signContent = signContent.concat(ossHeaders);

    signContent.push(buildCanonicalizedResource(resourcePath, request.parameters));

    return signContent.join('\n');
}

function signUtils_authorization(accessKeyId, accessKeySecret, canonicalString) {
    return 'OSS ' + accessKeyId + ':' + computeSignature(accessKeySecret, canonicalString);
}

function computeSignature(accessKeySecret, canonicalString) {
    var signature = crypto.createHmac('sha1', accessKeySecret);
    return signature.update(new Buffer(canonicalString, 'utf8')).digest('base64');
}

function authorization(method, resource, subres, headers, accessKeyId, accessKeySecret) {
    var stringToSign = canonicalString(method.toUpperCase(), resource, {
        headers: headers,
        parameters: subres
    });

    // accessKeyId = "STS.NUWRXB9zujsZx9719JFZvnLDm"

    // accessKeySecret = "7KHoPmpvBbDYRdGWYPt6T9nCxKqxFb2BqxH3ifQdnN6Y"

    return signUtils_authorization(accessKeyId, accessKeySecret, stringToSign);
}

function main(securityToken, accessKeyId, accessKeySecret, keys, x_ss_date) {
    headers = {
        "Content-Length": 45793,
        "Content-Type": "image/jpeg",
        "User-Agent": "aliyun-sdk-js/5.2.0 Chrome 81.0.4044.122 on OS X 10.15.5 64-bit",
        // "authorization": "OSS STS.NUYTaAJFXtyPyngEpLrSmAaiF:hbt4RDqtP7E8B5ZVKd9bRvQx4Ks=",
        "x-oss-date": x_ss_date,
        // "x-oss-date": "Sun, 03 May 2020 02:08:32 GMT",
        "x-oss-security-token": securityToken,
        "x-oss-user-agent": "aliyun-sdk-js/5.2.0 Chrome 81.0.4044.122 on OS X 10.15.5 64-bit"
    }
    resource = "/mgtv-bbqn/" + keys + ".jpeg"
    subres = undefined
    method = "PUT"

    return authorization(method, resource, subres, headers, accessKeyId, accessKeySecret)
}

// var sign = main()
// console.log({ sign: sign, date: x_ss_date })

// express暴露服务
const express = require("express")
const bodyParser = require("body-parser")
const app = express()

app.use(bodyParser.urlencoded({
    extended: false
}))
app.post("/getsign", function (req, resp, next) {

    var result = req.body
    let accessKeyId = result.accessKeyId
    let accessKeySecret = result.accessKeySecret
    let securityToken = result.securityToken
    let keys = result.keys

    let x_ss_date = dateFormat(+new Date() + 0, 'UTC:ddd, dd mmm yyyy HH:MM:ss \'GMT\'')


    let res = {
        'auth': main(securityToken, accessKeyId, accessKeySecret, keys, x_ss_date),
        'date': x_ss_date
    }
    console.log(res)
    resp.json(res)
})

app.listen(3000, () => {
    console.log("listening: 3000")
})