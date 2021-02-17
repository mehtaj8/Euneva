import React, { FunctionComponent } from 'react';
import './Navigation.css';

export const Navigation: FunctionComponent = () => {
  return (
    <div className='root-navigation-container'>
      <div className='todolist-title-collection-container'>
        <div className='todolist-title-collection-label'>My List</div>
        <div className='todolist-title-collection'>Collection of Titles</div>
        <div className='add-todolist-button-container'>
          <button>Add Todo</button>
        </div>
      </div>
    </div>
  );
};
