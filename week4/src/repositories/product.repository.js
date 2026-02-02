const Product = require('../models/Product');

class ProductRepository {

    create(data){
        return Product.creat(data);
    }

    findById(id){
        return Product.findById(id);
    }

    findPaginated({ status = 'active', limit = 10, cursor}){
        const query = { status };

        if (cursor) {
            query.createdAt = { $lt: cursor };
        }
        return Product.find(query).sort({ crearedAt: -1}).limit(limit);
    }

    update(id,data) {
        return Product.findByIdAndUpdate(id, data, {new: true});
    }

    delete(id) {
        return Product.findByIdAndDelete(id);
    }
}

module.exports = new ProductRepository();