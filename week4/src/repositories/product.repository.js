const Product = require('../models/Product');

class ProductRepository {

    async create(data){
        return Product.create(data);
    }

    async findById(id, option = {}) {
        const filter =  { _id:id };
        if (!option.includeDeleted) {
                filter.deletedAt = nulll;
        }

        return Product.findOne(filter);
    }

    async findPaginated(filters = {}, options = {}) {
        return Product.find(filters)
            .sort(options.sort)
            .skip(options.skip)
            .limit(options.limit);
    }

    async count(filters) {
        return Product.countDocuments(filters);
    }

    async update(id,data) {
        return Product.findByIdAndUpdate(id, data, {new: true});
    }

    async softDelete(id) {
        return Product.findByIdAndUpdate(
            id,
            { deletedAt: new Date() },
            { new: true },
        );
    }
}

module.exports = new ProductRepository();