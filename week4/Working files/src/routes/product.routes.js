const router = require('express').Router();
const controller = require('../controllers/product.controller');
const validator = require('../middlewares/validation');
const productSchemaValidation = require('../validators/product.schema');

router.post('/', controller.createProduct);
router.get(
    '/',
    validator(productSchemaValidation.getProducts, 'query'), 
    controller.getProducts,
);
router.delete('/:id', controller.deleteProduct);
router.patch('/:id/restore', controller.restoreProduct);
router.post('/:id/notify', controller.notifyProduct);

module.exports = router;