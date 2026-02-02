const { type, status } = require('express/lib/response');
const mongoose = require('mongoose');

const productSchema = new mongoose.Schema(
    {
        name: {
            type: String,
            required: true,
            trim: true,
        },
        price: {
            type: Number,
            required: true,
            min: 0,
        },
        ratings: {
            type: [Number],
            default: [],
        },
        status: {
            type: String,
            enum: ['active','inactive'],
            default: 'active',
        }
    },
    {
        timestamps: true,
        toJSON: {virtuals: true},
        toObject: {virtuals: true},
    }
);

productSchema.virtual('averageRating').get(function () {
    if (!this.ratings.length) return 0;
    return ( 
        this.ratings.reduce((sum,r) => sum+r, 0) / this.ratings.length
    );
});

module.exports = mongoose.model('Product', productSchema);