import { TodoItemType, TodoListType } from './type';

export interface ITodoItemProps {
  _id: string;
  _listId: string;
  title: string;
  isComplete: boolean;
  updateTodoItemTitleHandler: (
    event: React.KeyboardEvent<HTMLInputElement>,
    updatedTodoItemId: string,
    updatedTodoItemTitle: string,
  ) => void;
  updateTodoItemCompletionStatusHandler: (updatedTodoItemId: string) => void;
}

export interface ITodoListProps {
  _id: string;
  title: string;
  todoItemsCollection: TodoItemType[];
  setTodoListTitleState: (updatedTodoListTitle: string) => void;
  updateTodoListTitleHandler: (keyPressed: React.KeyboardEvent<HTMLInputElement>) => void;
  createTodoListHandler: () => void;
}

export interface IMainProps {
  getTodoListHandler: (event: React.KeyboardEvent<HTMLInputElement>) => void; // Presses Enter and Files Request
  updateTodoListTitleToRequest: (todoListNameToSearch: string) => void; // Everynew Input
  createTodoListHandler: () => void;
  todoListNameToSearch: string;
  todoList: TodoListType;
}
