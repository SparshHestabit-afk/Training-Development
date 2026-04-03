const router = require('express').Router();
const controller = require('../controllers/user.controller');

router.post('/', controller.createUser);
router.get('/', controller.getAllUsers,
);
router.get('/:id', controller.getUser);

module.exports = router;