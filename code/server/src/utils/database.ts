import mongoose from 'mongoose';

const connection = () => {
    console.log('Database Connection Pending...');

    const uri = `mongodb+srv://${process.env.DEV_DB_USERNAME}:${process.env.DEV_DB_PASSWORD}@cluster0.0eeps.mongodb.net/Cluster0?retryWrites=true&w=majority`;

    return mongoose.connect(uri, {
        useNewUrlParser: true,
        useUnifiedTopology: true
    });
};

export default connection;
