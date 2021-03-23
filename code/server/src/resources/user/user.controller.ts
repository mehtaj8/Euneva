import { Request, Response } from 'express';

// Activate venv prior to running server
export const getAvenueData = () => {
    return async (request: Request, response: Response) => {
        const { exit } = require('process');
        var exec = require('child_process').execSync;
        exec('cd ../../../');
        var result = exec(
            `python3 ./python_files/scrapeAvenue.py ${request.query.username} ${request.query.password}`
        );
        var stringData = result.toString('utf8');
        stringData.replace(/'/g, '"');
        return response.status(200).json({
            data: JSON.parse(stringData)
        });
    };
};
