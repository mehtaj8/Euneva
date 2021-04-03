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
    console.log('Beginning Avenue Scraping!');
    return async (request: Request, response: Response) => {
        const { exit } = require('process');
        var exec = require('child_process').execSync;
        exec('cd ../../../');
        var result = exec(
            `python3 ./python_files/scrapeAvenue.py ${request.query.username} ${request.query.password}`
        );
        var stringData = result.toString('utf8');
        stringData.replace(/'/g, '"');
        const scrapedData: ScrapedData = JSON.parse(stringData);
        try {
            for (let i = 0; i < scrapedData.data.TodoList.length; i++) {
                const todoList = scrapedData.data.TodoList[i];
                const listModelExists = await ListModel.findOne({
                    title: `${todoList.title}-macid-password`
                });

                if (!listModelExists) {
                    let listModelDocument = await ListModel.create({
                        title: `${todoList.title}-macid-password`,
                        description: todoList.description
                    });

                    for (
                        let j = 0;
                        j < todoList.todoItemsCollection.length;
                        j++
                    ) {
                        const todoItem = todoList.todoItemsCollection[j];
                        const itemModelDocument = await ItemModel.create({
                            _listId: listModelDocument._id,
                            title: todoItem.title,
                            description: todoItem.description,
                            isComplete: todoItem.isComplete,
                            dueDate: todoItem.dueDate
                        });
                    }
                } else {
                    for (
                        let j = 0;
                        j < todoList.todoItemsCollection.length;
                        j++
                    ) {
                        const todoItem = todoList.todoItemsCollection[j];
                        const itemModelDocument = await ItemModel.create({
                            _listId: listModelExists?._id,
                            title: todoItem.title,
                            description: todoItem.description,
                            isComplete: todoItem.isComplete,
                            dueDate: todoItem.dueDate
                        });
                    }
                }
            }
            console.log('Pushed to Database!');
            return response.status(200).send(scrapedData);
        } catch (e) {
            return response.status(400).send(e);
        }
    };
};
