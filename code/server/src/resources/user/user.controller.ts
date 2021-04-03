import { Request, Response } from 'express';
import { ItemModel } from '../item/item.model';
import { ListModel } from '../list/list.model';

type TodoList = {
    _id: string;
    title: string;
    description: string;
    creationDate: string;
    todoItemsCollection: {
        _id: string;
        _listId: string;
        title: string;
        description: string;
        creationDate: string;
        dueDate: string;
        isComplete: boolean;
    }[];
};

type ScrapedData = {
    user: { username: string; password: string };
    data: {
        TodoList: TodoList[];
    };
};
// comment

// Activate venv prior to running server
export const getAvenueData = () => {
    return async (request: Request, response: Response) => {
        const { exit } = require('process');
        var exec = require('child_process').execSync;
        exec('cd ../../../');
        var result = exec(
            `python3 ./python_files/scrapeAvenue.py ${request.query.username} ${request.query.password}`
        );
        var stringData = result.toString('utf8');
        stringData.replace(/'/g, '"');
        return response.status(200).json({
            data: JSON.parse(stringData)
        });
    };
};
