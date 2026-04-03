const productRepository = require('../repositories/product.repository');

class ProductService {
    
    //creating product logic
    async createProduct(data) {
        return productRepository.create(data);
    }

    //fetching product logic
    async getProducts(query) {
        const {
            search,
            minPrice,
            maxPrice,
            tags,
            sort,
            status,
            ratings,
            page = 1,
            limit = 10,
            includeDeleted = 'false'
        } = query;

        const filters = {};
        const options = {};

        //Deleted Object or document Verification (includeDeleted filter)
        if (!includeDeleted) {
            filters.deletedAt = null;
        }

        //Search filter
        if (search !== undefined && typeof search !== 'string') {
            const err = new Error('Invalid search parameter');
            err.statusCode = 400;
            err.code = 'INVALID_QUERY';
            throw err;
        }

        if (typeof search === 'string' && search.trim().length > 0) {
            const escaped = search.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            const regex = new RegExp(escaped, 'i');

            filters.$or = [
                { name: regex },
                { description: regex },
            ]
        }

        //Price filter usign Min. Price and Max. Price
        if (minPrice || maxPrice) {
            filters.price = {};
            if (minPrice) filters.price.$gte = Number(minPrice);
            if (maxPrice) filters.price.$lte = Number(maxPrice);
        }

        //tags filter
        if (tags) {
            const tagsArray = Array.isArray(tags) 
            ? tags 
            : tags.split(',').map(t => t.trim());
            
            filters.tags = { $in: tagsArray};
        }

        //status filter
        if (status) {
            const statusArray = Array.isArray(status) 
            ? status
            : status.split(',').map(s => s.trim());

            filters.status = { $in: statusArray};
        }

        //sorting filter
        if (sort) {
            const [field, order] = sort.split(':');
            options.sort = { [field]: order === 'desc' ? -1 : 1 };
        } else {
            options.sort = { createdAt: -1 };
        }

        //pages and limit filter
        const pageNum = Math.max(Number(page) || 1, 1);
        const limitNum = Math.min(Number(limit) || 10, 50);

        options.limit = limitNum;
        options.skip = (pageNum - 1) * limitNum;

        //returning the filtered data
        const [data, total] = await Promise.all([
            productRepository.findPaginated(filters, options),
            productRepository.count(filters),
        ]);

        return {
            data: Array.isArray(data) ? data : [],
            pagination: {
                total: total || 0,
                page: pageNum,
                limit: limitNum,
                pages: Math.ceil((total || 0) / limitNum),
            },
        };
    }

    //deleting product logic
    async deleteProduct(id) {
        return productRepository.softDelete(id);
    }

    //restoring product logic
    async restoreProduct(id) {
        const product = await productRepository.findById(id, { includeDeleted: true });

        if (!product || product.deletedAt === null) {
            return null;
        }

        return productRepository.restore(id);
    }

}

module.exports = new ProductService();