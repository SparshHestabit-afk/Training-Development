const productService = require('../services/product.service');

class ProductController {
    async getProducts(req, res, next) {
        try{
            const result = await productService.getProducts(req.query);
            res.status(200).json({ 
                success: true,
                message: 'Products fetched successfully',
                data: result.data || [],
                pagination: result.pagination
            });
        } catch (err) {
            next(err);
        }
    }

    async deleteProduct(req, res, next) {
        try {
            const deletedProduct = await productService.deleteProduct(req.params.id);

            if(!deletedProduct) {
                return res.status(404).json({
                    success: false,
                    message: 'Products not found',
                    code: 'PRODUCT_NOT_FOUND'
                });
            }

            return res.status(200).json({
                success: true,
                message: 'Products deleted successfully',
                data: {
                    id: deletedProduct._id,
                    deletedAt: deletedProduct.deletedAt,
                }
            });

        } catch (err) {
            next(err);
        }
    }

    async restoreProduct(req, res, next) {
        try {
            const restoredProduct = await productService.restoreProduct(req.params.id);

            if(!restoredProduct) {
                return res.status(404).json({
                    success: false,
                    message: 'Product not found',
                    code: 'PRODUCT_NOT_FOUND',
                });
            }

            return res.status(200).json({
                success: true,
                message: 'Product restored Successfully',
                data: {
                    id: restoredProduct._id,
                    restoredAt: new Date(),
                }
            });
            
        } catch (err) {
            next(err);
        }
    }
}

module.exports = new ProductController();