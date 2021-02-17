import React, { FunctionComponent, useState } from 'react';
import { Main } from './Components/MainComponentFolder/Main';
import { TodoItemType, TodoListType } from './type';
import { API } from './constants';
import { getTodaysDate } from './Utility/getTodaysDate';

export const App: FunctionComponent = () => {
  const [todoListTitleToRequest, setTodoListTitleToRequest] = useState('');
  const [todoList, setTodoList] = useState<TodoListType>({
    _id: '',
    title: '',
    creationDate: '',
    description: '',
    todoItemsCollection: [],
  });

  const getTodoListHandler = async (event: React.KeyboardEvent<HTMLInputElement>): Promise<void> => {
    if (event.key === 'Enter') {
      const todoListResponse = await getTodoListTitleRequest(todoListTitleToRequest);
      const todoItemsCollectionResponse = await getTodoItemsRequest(todoListResponse._id);
      const incompleteTodoItemCollection = todoItemsCollectionResponse.filter(todoItem => {
        if (!todoItem.isComplete) return todoItem;
      });
      setTodoList({
        _id: todoListResponse._id,
        title: todoListResponse.title,
        creationDate: todoListResponse.creationDate,
        description: todoListResponse.description,
        todoItemsCollection: incompleteTodoItemCollection,
      });
    }
  };

  const createTodoListHandler = async () => {
    const response = await createTodoListRequest();
    setTodoList({
      _id: response._id,
      title: response.title,
      creationDate: response.creationDate,
      description: response.description,
      todoItemsCollection: [],
    });
  };
  // search component, stores data user has input to search, recieves a prop function when user triggers search
  // keep the request for the list in this top level (this component)
  // list component, not rendered if list is undefined, prop list id, gets list elements within this component

  return (
    <main>
      <Main
        key={todoList._id}
        getTodoListHandler={getTodoListHandler}
        updateTodoListTitleToRequest={setTodoListTitleToRequest}
        todoListNameToSearch={todoListTitleToRequest}
        todoList={todoList}
        createTodoListHandler={createTodoListHandler}
      />
    </main>
  );
};

// GET readOneList
const getTodoListTitleRequest = async (todoListTitle: string): Promise<TodoListType> => {
  try {
    const endpoint = `${API}list/${todoListTitle}`;
    const response: Response = await fetch(endpoint);
    // if (response.status >= 200 && response.status < 300) {
    const { data } = await response.json();
    return data;
  } catch (error) {
    console.log(error);
    return error;
  }
};

// GET readAllItemsFromList
const getTodoItemsRequest = async (todoListId: string): Promise<TodoItemType[]> => {
  try {
    const endpoint = `${API}items/?_listId=${todoListId}`;
    const response = await fetch(endpoint);
    const { data } = await response.json();
    return data;
  } catch (error) {
    console.log(error);
    return error;
  }
};

// POST createOneList
const createTodoListRequest = async (): Promise<TodoListType> => {
  const endpoint = `${API}list/`;
  try {
    const date = getTodaysDate();
    console.log(date);
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title: `Fake-Title-${date}`,
        description: '',
      }),
    });
    const { data } = await response.json();
    return data;
  } catch (error) {
    console.log(error);
    return error;
  }
};
