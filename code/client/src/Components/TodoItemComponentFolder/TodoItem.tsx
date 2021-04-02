import { useState } from 'react';
import React, { FunctionComponent } from 'react';
import { ITodoItemProps } from '../../props';
import './TodoItem.css';

export const TodoItem: FunctionComponent<ITodoItemProps> = (props: ITodoItemProps) => {
  const [todoItemTitleState, setTodoItemTitleState] = useState(props.title);

  return (
    <div className='todoitem-container'>
      <div className='todoitem-completion-button-container'>
        <input
          type='checkbox'
          checked={props.isComplete}
          className='todoitem-completion-button'
          onChange={() => props.updateTodoItemCompletionStatusHandler(props._id)}
        />
      </div>
      <div className={'todoitem-information-container'}>
        <input
          type={'text'}
          className={'todoitem-title'}
          placeholder={'Add Todo Item'}
          value={todoItemTitleState}
          onChange={e => {
            setTodoItemTitleState(e.target.value);
          }}
          onKeyPress={e => props.updateTodoItemTitleHandler(e, props._id, todoItemTitleState)}
        />
      </div>
    </div>
  );
};
