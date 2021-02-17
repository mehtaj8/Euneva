export type TodoItemType = {
  _id: string;
  _listId: string;
  title: string;
  description?: string;
  creationDate: string;
  dueDate?: string;
  isComplete: boolean;
};

export type TodoListType = {
  _id: string;
  title: string;
  description?: string;
  creationDate: string;
  todoItemsCollection: TodoItemType[];
};

export type TodoListAPIType = {
  message: string;
  data: TodoListType;
};
