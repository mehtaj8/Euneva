import { Router } from 'express';
import { getAvenueData } from './user.controller';

export const userRouter = Router();

userRouter.route('/').get(getAvenueData());
