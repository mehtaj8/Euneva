import mongoose from 'mongoose';
import { model, Schema } from 'mongoose';
import { getTodaysDate } from '../../utils/getTodayDate';

export const ItemSchema: Schema = new Schema({
    _listId: {
        type: mongoose.SchemaTypes.ObjectId,
        ref: 'List',
        required: true
    },
    title: {
        type: String,
        trim: true,
        maxlength: 60
    },
    description: {
        type: String,
        trim: true,
        maxlength: 50
    },
    creationDate: {
        type: String,
        default: getTodaysDate()
    },
    dueDate: {
        type: Date
    },
    isComplete: {
        type: Boolean,
        default: false
    }
});

export const ItemModel = model('Item', ItemSchema);
