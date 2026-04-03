const { type, status } = require('express/lib/response');
const mongoose = require('mongoose');

const productSchema = new mongoose.Schema(
    {
        name: {
            type: String,
            required: true,
            trim: true,
        },
        description: {
            type: String,
            trim: true,
        },
        price: {
            type: Number,
            required: true,
            min: 0,
        },
        tags: {
            type: [String],
            index: true,
        },
        ratings: {
            type: [Number],
            default:[],
        },
        status: {
            type: String,
            enum: ['Active','Inactive'],
            default: 'Active',
        },
        deletedAt: {
            type: Date,
            default: null
        },
    },
    {
        timestamps: true,
        toJSON: {virtuals: true},
        toObject: {virtuals: true},
    }
);

productSchema.virtual('averageRating').get(function () {
    if (!Array.isArray(this.ratings) || this.ratings.length === 0) return 0;
    return this.ratings.reduce((sum,r) => sum+r, 0) / this.ratings.length;
});

productSchema.index({ status: 1, createdAt: -1 });

module.exports = mongoose.model('Product', productSchema);