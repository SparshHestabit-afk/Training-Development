const productRepository = require('../repositories/product.repository');

class ProductService {

    async getProducts(query) {
        const {
            search,
            minPrice,
            maxPrice,
            tags,
            sort,
            page = 1,
            limit = 10,
            includeDeleted
        } = query;

        const filters = {};
        const options = {};

        if (includeDeleted !== 'true') {
            filters.deletedAt = null;
        }

        if (search) {
            const escaped = search.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            const regex = new RegExp(escaped, 'i');
            filters.$or = [
                { name: regex },
                { description: regex },
            ]
        }

        if (minPrice || maxPrice) {
            filters.price = {};
            if (minPrice) filters.price.$gte = Number(minPrice);
            if (maxPrice) filters.price.$lte = Number(maxPrice);
        }

        if (tags) {
            filters.tags = { $in: tags.split(',') };
        }

        if (sort) {
            const [field, order] = sort.split(':');
            options.sort = { [field]: order === 'desc' ? -1 : 1 };
        } else {
            options.sort = { createdAt: -1 };
        }

        const pageNum = Math.max(Number(page) || 1, 1);
        const limitNum = Math.min(Number(limit) || 10, 50);

        options.limit = limitNum;
        options.skip = (pageNum - 1) * limitNum;

        const [data, total] = await Promise.all([
            productRepository.findPaginated(filters, options),
            productRepository.count(filters),
        ]);

        return {
            data,
            pagination: {
                total,
                page: pageNum,
                limit: limitNum,
                pages: Math.ceil(total / limitNum),
            },
        };
    }

    async deleteProduct(id) {
        return productRepository.softDelete(id);
    }

    async restoreProduct(id) {
        return productRepository.restore(id);
    }
}

module.exports = new ProductService();