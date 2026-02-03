const Product = require('../models/Product');

class ProductRepository {

    async create(data) {
        return Product.create(data);
    }

    async findById(id, option = {}) {
        const filter = { _id: id };

        if (!option.includeDeleted) {
            filter.deletedAt = null;
        }

        return Product.findOne(filter).lean();
    }

    async findPaginated(filters = {}, options = {}) {
        return Product.find(filters)
            .sort(options.sort || { createdAt: -1 })
            .skip(options.skip || 0)
            .limit(options.limit || 10)
            .lean();
    }

    async count(filters) {
        return Product.countDocuments(filters);
    }

    async update(id, data) {
        return Product.findByIdAndUpdate(id, data, { new: true, runValidators: true, }).lean();
    }

    async softDelete(id) {
        return Product.findByIdAndUpdate(
            id,
            { deletedAt: new Date() },
            { new: true },
        ).lean();
    }

    async restore(id) {
        return Product.findByIdAndUpdate(
            id,
            {deletedAt: null},
            {new: true},
        ).lean();
    }
}

module.exports = new ProductRepository();