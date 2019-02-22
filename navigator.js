/*
 * Author:         Austin Moore
 * Script Type:    Main Script
 * Description:    A queue system for queueing websites and specific actions to be
 *                 performed on them
 * Notes:          In development. This script is intended to run website-action
                   queues with Node.js companion scripts.
 * Packages:       readline-sync
 */

 class queue
 {
    constructor(web_queue, action_queue, web_action_queue)
    {
        this.web_queue = web_queue;
        this.action_queue = action_queue;
        this.web_action_queue = web_action_queue;
    }
 }

function is_numeric(value)
{
    return !isNaN(value);
}

function load_queue(queues, queue_type)
{
    switch(queue_type)
    {
        case "web_action_queue": 
            let fs = require("fs");
            fs.readdirSync("./web-action-queues/").forEach(file => {
                console.log(file);
            });
            break;
        default: process.exit(1); // This would be my fault
    }
}

function load_queue_menu(queues)
{
    let input = "";

    while (input === "")
    {
        console.log("\n----------------------------------------------------")
        console.log("1.  Load website-action queue");
        console.log("2.  Back")
        console.log("----------------------------------------------------")

        input = readline_sync.question("\nSelect an option: ");

        if (is_numeric(input) === true)
        {
            input = parseInt(input);

            switch(input)
            {
                case 1: load_queue(queues, "web_action_queue");
                        break;
                case 2: return;                  
                default: console.log("Invalid number.");
                         input = "";
                         continue;                
            }
        }
        else
        {
            input = "";
            continue;
        }
    }
}

function menu(queues)
{
    let input = "";

    while (input === "")
    {
        console.log("\n----------------------------------------------------")
        console.log("1.  Load a queue");
        console.log("2.  Print a queue");
        console.log("3.  Run website-action queue");
        console.log("4.  Quit")
        console.log("----------------------------------------------------")

        input = readline_sync.question("\nSelect an option: ");

        if (is_numeric(input) === true)
        {
            input = parseInt(input);

            switch(input)
            {
                case 1: load_queue_menu(queues);
                        input = "";
                        continue;
                case 4: process.exit(0);
                default: console.log("Invalid number."); 
                         input = "";
                         continue;
            }
        }
        else
        {
            input = "";
            continue;
        }
    }
}

const readline_sync = require("readline-sync");
let queues = new queue([], [], [[]]);
menu(queues)
