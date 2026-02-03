const router = require('express').Router();
const controller = require('../controllers/product.controller');

router.get('/products', controller.getProducts);
router.delete('/products/:id', controller.deleteProduct);
router.patch('/products/:id/restore', controller.restoreProduct);

module.exports = router;