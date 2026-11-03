const images = require('./_email-assets');
module.exports = (req,res) => {
 if (req.method !== 'GET' && req.method !== 'HEAD') return res.status(405).end();
 const id=String(req.query.image || '');
 if (!Object.prototype.hasOwnProperty.call(images,id)) return res.status(404).end();
 res.setHeader('Content-Type',id==='logo'?'image/png':'image/jpeg');
 res.setHeader('Cache-Control','public, max-age=604800');
 res.setHeader('X-Content-Type-Options','nosniff');
 return res.status(200).end(req.method==='HEAD'?undefined:Buffer.from(images[id],'base64'));
};
