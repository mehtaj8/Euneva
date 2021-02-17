import React, { FunctionComponent, useState } from 'react';
import { API } from '../../constants';
import { ITodoListProps } from '../../props';
import { TodoItemType } from '../../type';
import { TodoItem } from '../TodoItemComponentFolder/TodoItem';
import './TodoList.css';

export const TodoList: FunctionComponent<ITodoListProps> = (props: ITodoListProps) => {
  const [todoItemsCollection, setTodoItemsCollection] = useState(props.todoItemsCollection);

  // Function to update the TodoItem information in local state & database
  const updateTodoItemTitleHandler = async (
    event: React.KeyboardEvent<HTMLInputElement>,
    updatedTodoItemId: string,
    updatedTodoItemTitle: string,
  ) => {
    if (event.key === 'Enter') {
      // API Request to update TodoItem in DB goes HERE
      setTodoItemsCollection(
        todoItemsCollection.map(todoItem => {
          if (todoItem._id === updatedTodoItemId) {
            todoItem.title = updatedTodoItemTitle;
          }
          return todoItem;
        }),
      );
      await updateTodoItemRequest(updatedTodoItemId, { title: updatedTodoItemTitle });
    }
  };

  const updateTodoItemCompletionStatusHandler = async (updatedTodoItemId: string) => {
    // API Request to update TodoItem in DB goes HERE
    setTodoItemsCollection(
      todoItemsCollection.filter(todoItem => {
        return todoItem._id !== updatedTodoItemId;
      }),
    );
    await updateTodoItemRequest(updatedTodoItemId, { isComplete: true });
  };

  const addNewTodoItem = async () => {
    // API Request to create a TodoItem in DB
    // Once API Request is complete, retrieve the new item details and put it into the array
    if (todoItemsCollection.filter(todoItem => !todoItem.title).length > 0) {
      alert('We have already created another Todo Item. Fill that out first.');
      return;
    }

    // Temp Stuff being placed in TodoItems[]
    const newTodoItem: TodoItemType = await createTodoItemRequest(props._id);
    const newTodoItemCollection = [...todoItemsCollection];
    newTodoItemCollection.push(newTodoItem);
    setTodoItemsCollection(newTodoItemCollection);
  };

  const renderTodoListInformation = () => {
    if (props._id) {
      return (
        <div className='todolist-information-container'>
          <input
            className='todolist-title'
            value={props.title}
            placeholder={'Todo List Title'}
            onChange={e => props.setTodoListTitleState(e.target.value)}
            onKeyPress={e => props.updateTodoListTitleHandler(e)}
          />
          <div className='todolist-uncompleted-item-count'>{todoItemsCollection.length}</div>
        </div>
      );
    }

    return (
      <div className='todolist-information-container'>
        <h1 className='todolist-title'>Create or Find a List</h1>
      </div>
    );
  };

  // Determines when to render the Add Item Button
  const renderAddItemButton = () => {
    if (props._id) {
      return (
        <button className={'add-todoitem-button'} onClick={addNewTodoItem}>
          Add Item
        </button>
      );
    }
  };

  return (
    <div className='root-todolist-container'>
      <div className='todolist-buttons-container'>
        {renderAddItemButton()}
        <button className={'add-todoitem-button'} onClick={props.createTodoListHandler}>
          Create New List
        </button>
      </div>
      {renderTodoListInformation()}
      <div className='todolist-todoitem-collection-container'>
        {todoItemsCollection.map(todoItem => {
          return (
            <TodoItem
              key={todoItem._id}
              _id={todoItem._id}
              _listId={todoItem._listId}
              title={todoItem.title}
              isComplete={todoItem.isComplete}
              updateTodoItemTitleHandler={updateTodoItemTitleHandler}
              updateTodoItemCompletionStatusHandler={updateTodoItemCompletionStatusHandler}
            />
          );
        })}
      </div>
    </div>
  );
};

// PUT updateOneItem
const updateTodoItemRequest = async (itemId: string, updatedItem: any) => {
  const endpoint = API + `items/${itemId}`;
  try {
    const response = await fetch(endpoint, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        _id: itemId,
        ...updatedItem,
      }),
    });
    const { data } = await response.json();
    return data;
  } catch (error) {
    console.log(error);
    return error;
  }
};

// POST createOneItem
const createTodoItemRequest = async (_listId: string) => {
  const endpoint = API + `items/`;
  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        _listId: _listId,
        title: ' ',
        description: ' ',
      }),
    });
    const { data } = await response.json();
    return data;
  } catch (error) {
    console.log(error);
    return error;
  }
};
