import { Request, Response } from 'express';
import { ListModel } from './list.model';

// POST Request
export const createOneList = (listModel: typeof ListModel) => {
    return async (request: Request, response: Response) => {
        try {
            const document = await listModel.create(request.body);
            return response.status(201).json({
                message: 'This list has successfully been created',
                data: document
            });
        } catch (error) {
            return response.status(400).send(error);
        }
    };
};

// GET Request
export const readOneList = (listModel: typeof ListModel) => {
    return async (request: Request, response: Response) => {
        console.log(request);
        try {
            const document = await listModel.findOne({
                title: request.params.title
            });
            if (document) {
                console.log(document);
                return response.status(200).json({
                    message:
                        'This requested list has successfully been retrieved.',
                    data: document
                });
            }

            return response.status(404).json({
                message: 'The requested list does not exist'
            });
        } catch (error) {
            return response.status(400).send(error);
        }
    };
};

// PUT Request
export const updateOneList = (listModel: typeof ListModel) => {
    return async (request: Request, response: Response) => {
        try {
            const document = await listModel.findOneAndUpdate(
                { title: request.params.title },
                request.body,
                { new: true }
            );
            if (document) {
                return response.status(200).json({
                    message: 'The specified list has successfully been updated',
                    data: document
                });
            }

            return response.status(404).json({
                message: 'The specified list was unable to be updated.'
            });
        } catch (error) {
            return response.status(400).send(error);
        }
    };
};

// DELETE Request
export const deleteOneList = (listModel: typeof ListModel) => {
    return async (request: Request, response: Response) => {
        try {
            const document = await listModel.findOneAndDelete({
                title: request.params.title
            });
            if (document !== null) {
                return response.status(200).json({
                    message:
                        'The specified list has successfully been deleted.',
                    data: document
                });
            } else {
                return response.status(400).json({
                    message:
                        'The specified list has already been deleted in the past'
                });
            }
        } catch (error) {
            return response.status(400).send(error);
        }
    };
};

// DELETE Request
export const deleteAllLists = (listModel: typeof ListModel) => {
    return async (request: Request, response: Response) => {
        try {
            const document = await listModel.deleteMany({});
            return response.status(200).json({
                message: 'All lists have successfully been deleted',
                data: document
            });
        } catch (error) {
            return response.status(400).send(error);
        }
    };
};
