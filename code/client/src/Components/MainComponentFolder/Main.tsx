import React, { FunctionComponent, useState } from 'react';
import './Main.css';
import { TodoList } from '../TodoListComponentFolder/TodoList';
import { IMainProps } from '../../props';
import { API } from '../../constants';
import { TodoListType } from '../../type';

export const Main: FunctionComponent<IMainProps> = (props: IMainProps) => {
  const [todoListTitleState, setTodoListTitleState] = useState(props.todoList.title);

  // Function that determines when to send the PUT Request to update TodoList title
  const updateTodoListTitleHandler = async (keyPressed: React.KeyboardEvent<HTMLInputElement>) => {
    if (keyPressed.key === 'Enter') {
      // API Call to Update Todo List Title
      await updateTodoListRequest(props.todoList.title, todoListTitleState, props.todoList._id);
    }
  };

  return (
    <div className='root-container'>
      <TodoList
        key={props.todoList._id}
        title={todoListTitleState}
        todoItemsCollection={props.todoList.todoItemsCollection}
        _id={props.todoList._id}
        setTodoListTitleState={setTodoListTitleState}
        updateTodoListTitleHandler={updateTodoListTitleHandler}
        createTodoListHandler={props.createTodoListHandler}
      />

      <input
        className={'get-list-input-bar'}
        placeholder='Find your list'
        value={props.todoListNameToSearch}
        onChange={e => props.updateTodoListTitleToRequest(e.target.value)}
        onKeyPress={e => props.getTodoListHandler(e)}
      />
    </div>
  );
};

const updateTodoListRequest = async (
  currentTodoListTitle: string,
  newTodoListTitle: string,
  currentTodoListId: string,
): Promise<TodoListType> => {
  const endpoint = API + `list/${currentTodoListTitle}`;
  try {
    const response: Response = await fetch(endpoint, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        _id: currentTodoListId,
        title: newTodoListTitle,
      }),
    });
    const { data } = await response.json();
    return data;
  } catch (error) {
    console.log(error);
    return error;
  }
};
