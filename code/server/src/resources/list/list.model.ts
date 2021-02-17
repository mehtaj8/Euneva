import { Schema, model } from 'mongoose';
import { getTodaysDate } from '../../utils/getTodayDate';
export const ListSchema: Schema = new Schema({
    title: {
        type: String,
        trim: true,
        maxlength: 40,
        unique: true
    },
    description: {
        type: String,
        trim: true,
        maxlength: 50
    },
    creationDate: {
        type: String,
        default: getTodaysDate()
    }
});

ListSchema.index({ title: 1 }, { unique: true });

export const ListModel = model('List', ListSchema);
