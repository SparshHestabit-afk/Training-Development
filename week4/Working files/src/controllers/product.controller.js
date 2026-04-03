const productService = require('../services/product.service');
const logger = require('../utils/logger');
const { enqueueEmail } = require('../jobs/email.job');

class ProductController {
    
    async createProduct(req, res, next) {
        try {
            logger.info('Creating Product', req);

            const product = await productService.createProduct(req.body);
            logger.info(`Product created: ${product._id}`, req);

            res.status(201).json({
                success: true,
                message: 'Product created',
                data: product,
            });
        } catch (err) {
            logger.error(err.message, req);
            next(err);
        }
    }

    async getProducts(req, res, next) {
        try {

            logger.info('Fetching Products', req);

            const result = await productService.getProducts(req.query);
            logger.info('Products fetched successfully', req);
            res.status(200).json({
                success: true,
                message: 'Products fetched successfully',
                data: result.data || [],
                pagination: result.pagination
            });
        } catch (err) {
            logger.error(err.message, req)
            next(err);
        }
    }

    async deleteProduct(req, res, next) {
        try {
            logger.info('Deleting Product', req);

            const deletedProduct = await productService.deleteProduct(req.params.id);

            if (!deletedProduct) {
                return res.status(404).json({
                    success: false,
                    message: 'Products not found',
                    code: 'PRODUCT_NOT_FOUND'
                });
            }

            logger.info('Product Deleted Successfully', req)
            return res.status(200).json({
                success: true,
                message: 'Products deleted successfully',
                data: {
                    id: deletedProduct._id,
                    deletedAt: deletedProduct.deletedAt,
                }
            });

        } catch (err) {
            logger.error(err.message, req);
            next(err);
        }
    }

    async restoreProduct(req, res, next) {
        try {
            logger.info('Restoring product', req);

            const restoredProduct = await productService.restoreProduct(req.params.id);

            if (!restoredProduct) {
                return res.status(404).json({
                    success: false,
                    message: 'Product not found',
                    code: 'PRODUCT_NOT_FOUND',
                });
            }

            logger.info('Product restored successfully', req);

            return res.status(200).json({
                success: true,
                message: 'Product restored Successfully',
                data: {
                    id: restoredProduct._id,
                    rdeletedAt: restoredProduct.deletedAt,
                },
            });

        } catch (err) {
            logger.error(err.message, req);
            next(err);
        }
    }

    async notifyProduct(req, res, next) {
        try {
            logger.info('Notifying Product', req);

            const { userId } = req.body;
            const { id: productId } = req.params;

            if (!userId) {
                return res.status(400).json({
                    success: false,
                    message: 'User ID required',
                });
            }

            const job = await enqueueEmail({ userId, productId }, req);

            return res.status(202).json({
                success: true,
                message: 'Notification scheduled',
                jobId: job.id,
            });

        } catch (err) {
            logger.error(err.message, req);
            next(err);
        }
    }
}

module.exports = new ProductController();