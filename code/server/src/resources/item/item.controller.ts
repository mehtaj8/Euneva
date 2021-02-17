import { Request, Response } from 'express';
import { ItemModel } from './item.model';

// POST Request
export const createOneItem = (itemModel: typeof ItemModel) => {
    return async (request: Request, response: Response) => {
        //console.log(request);
        try {
            const document = await itemModel.create(request.body);
            console.log(document);
            console.log('Creating 1 Item...');
            return response.status(200).json({
                message: 'Item Successfully Created',
                data: document
            });
        } catch (err) {
            console.log(err);
            return response.status(400).send(err);
        }
    };
};

// GET Request - currently unneeded
export const readOneItem = (itemModel: typeof ItemModel) => {
    return async (request: Request, response: Response) => {
        try {
            const document = await itemModel.findById({
                _id: request.params._id
            });
            console.log('Getting 1 Item...');
            return response.status(200).json({
                message: 'The specified item has been found',
                data: document
            });
        } catch (error) {
            return response.status(400).send(error);
        }
    };
};

// Update Request
export const updateOneItem = (itemModel: typeof ItemModel) => {
    return async (request: Request, response: Response) => {
        try {
            const document = await itemModel.findByIdAndUpdate(
                request.params._id,
                request.body,
                { new: true }
            );
            console.log('Updating 1 Item..');
            return response.status(200).json({
                message: 'The specified item has been updated!',
                data: document
            });
        } catch (error) {
            return response.status(400).send(error);
        }
    };
};

// DELETE Request - currently unneeded
export const deleteOneItem = (itemModel: typeof ItemModel) => {
    return async (request: Request, response: Response) => {
        try {
            const document = await itemModel.deleteOne({
                _id: request.params._id
            });
            console.log('Deleting 1 Item...');
            return response.status(200).json({
                message: 'The specified item has successfully been deleted',
                data: document
            });
        } catch (error) {
            return response.status(400).send(error);
        }
    };
};

// GET Request
export const readAllItemsFromList = (itemModel: typeof ItemModel) => {
    return async (request: Request, response: Response) => {
        try {
            // const document = await itemModel.find().populate('List', {
            //     match: { _id: { $eq: request.body._listId } }
            // });
            // Why didn't populate work?
            const document = await itemModel.find({
                _listId: request.query._listId
            });
            if (document) {
                console.log('Retrieving all items');
                return response.status(200).json({
                    message:
                        'All items within this particular list have been retrieved',
                    data: document
                });
            }
        } catch (error) {
            return response.status(400).send(error);
        }
    };
};

// DELETE Request - currently unneeded
export const deleteAllItems = (itemModel: typeof ItemModel) => {
    return async (request: Request, response: Response) => {
        try {
            const document = await itemModel.deleteMany({});
            console.log('Deleting All Items...');
            return response.json({
                message: 'All Items have been deleted',
                data: document
            });
        } catch (err) {
            return response.status(400).send(err);
        }
    };
};
