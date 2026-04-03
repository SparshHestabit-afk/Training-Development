const {randomUUID} = require('crypto');

module.exports = function tracking(req, res, next) {
    const requestID = req.headers['x-request-id'] || randomUUID();

    req.requestId = requestID;
    res.setHeader('X-Request-ID', requestID);
    next();
}