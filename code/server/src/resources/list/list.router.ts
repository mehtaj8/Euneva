import { Router } from 'express';
import {
    createOneList,
    deleteOneList,
    readOneList,
    updateOneList
} from './list.controller';
import { ListModel } from './list.model';

const listRouter = Router();

listRouter.route('/').post(createOneList(ListModel)); // C)

listRouter
    .route('/:title')
    .get(readOneList(ListModel)) // R
    .put(updateOneList(ListModel)) // U
    .delete(deleteOneList(ListModel)); // D

export { listRouter };
