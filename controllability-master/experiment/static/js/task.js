/*
 * Requires:
 *     psiturk.js
 *     utils.js
 */

/*jslint browser: true*/
/*global _, $, d3, window, setTimeout, clearInterval, PsiTurk, uniqueId, adServerLoc, mode, condition, counterbalance */

// Initalize psiturk object
var psiTurk = new PsiTurk(uniqueId, adServerLoc, mode),
    EXP = {
        skipinstr: true,
        condition: parseInt(condition),
        counterbalance: parseInt(counterbalance),
        nactions: 6,
        std_bw: [0,1,2],
        std_wi: [0,1,2],
        rwdmean: 20,
        nblocks: 9,
        trialsperblock: 20,
        pages: [
            "instructions/instruct-1.html",
            "instructions/instruct-2.html",
            "stage.html",
            "postquestionnaire.html",
            "transition.html",
            "quiz.html",
            "restart.html"
        ],
        instructionPages: [
            "instructions/instruct-1.html",
            "instructions/instruct-2.html"
        ],
        loop: 0
    };


psiTurk.preloadPages(EXP.pages);

function quiz(instructions, callback) {
    "use strict";
    function record_responses() {
        var allRight = true;
        $("select").each(function () {
            psiTurk.recordTrialData({"phase": "INSTRUCTQUIZ", "question": this.id, "answer": this.value, "loop": EXP.loop});
            if (this.id === "grovessame" && this.value !== "no") {
                allRight = false;
            } else if (this.id === "numtrips" && this.value !== "thirty") {
                allRight = false;
            } else if (this.id === "distribution" && this.value !== "somepreferred") {
                allRight = false;
            } else if (this.id === "goal" && this.value !== "most") {
                allRight = false;
            }
        });
        return allRight;
    }
    psiTurk.showPage("quiz.html");
    $("#continue").click(function () {
        if (record_responses()) {
            // Record that the user has finished the instructions and
            // moved on to the experiment. This changes their status code
            // in the database.
            psiTurk.recordUnstructuredData("instructionloops", EXP.loop);
            psiTurk.finishInstructions();
            // Move on to the experiment
            callback();
        } else {
            EXP.loop += 1;
            psiTurk.showPage("restart.html");
            $(".continue").click(function () {
                psiTurk.doInstructions(
                    instructions,
                    function () {quiz(instructions, callback); }
                );
            });
        }
    });
}


function decisionProblem(params, callback) {
    "use strict";
    var stage,
        message,
        actiongroups,
        rewardgroups,
        actions,
        score = 0,
        RV = [params.R,params.V],
        R = params.R,
        V = params.V,
        ntrials = params.trials,
        trial = 0,
        rtTime;

    var rewardstodate = []; 
    for(var a = 0; a < R.length; a++) { rewardstodate.push([]);}

    // function paytoplay() {

    // }

    // function choicetask(params, callback){
    
    // }

    function setupPage() {
        stage = d3.select("body").select("svg");
        message = stage.append("text")
            .attr({x: 170, y: 20})
            .text("Choose a grove")
            .style("font", "20px monospace");

        actiongroups = stage.selectAll(".actionGroup")
            .data(RV)
            .enter()
            .append("g") // g for group
            .attr("id", function(d, i) {return "actgroup" + i; })
            .attr("transform", function(d, i) {
                return "translate(" + (50 + 110 * i) + ", " + (50) + ")"; // N actions horizontally spread across screen
            });


        actions = actiongroups.append("image")
            .attr("id", function(d, i) {return "action" + i; })
            .attr("class", "action")
            .attr("xlink:href", "static/images/0810.png") // Tree image for each action
            .attr({width: 100, height: 102}); // Pixel size of image

        actiongroups.append("text")
            .text(function(d, i) {return "Grove " + (i + 1); }) // Text labeling each grove
            .attr("x", "20")
            .attr("y", "115"); // Distance from topleft corner of each action group (height of img + 13)

        rwdgroups = stage.append('g')
            .selectAll('g')                 
            .data(rewardstodate)
            .enter()
            .append('g')
            .selectAll('circle')
            .data( function(d,i,j) { return d; } )
            .enter()
            .append('circle')
            .attr({
                r:20,
                cx: function(d,i,j) { return (j * 110) + 50; },
                cy: function(d,i,j) { return (i * 45) + 175; },
                fill: "#BADBDA",
                stroke: "#2F3550",
                'stroke-width': 2
        });

        rwdtext = stage.append('g') //removing
            .selectAll('g') 
            .data(rewardstodate)
            .enter()
            .append('g')
            .selectAll('text') // these
            .data( function(d,i,j) { return d; } ) //lines
            .enter() //text displays normally
            .append('text')
            .text( function(d,i,j) { return d; } )
            .attr('x', function(d,i,j) { return (j * 110) + 50; })
            .attr('y', function(d,i,j) { return (i * 45) + 175; })
            .style('font', '20px monospace');

        next();
    }


    function responseFn(d, i) {
        // When responseFn is called on action item i, d is RV
        var reward,
            rewardstodate,
            trialdata,
            i,
            j;
        actions.on("click", function () {}); // Listens for click on one of the actions
        d3.select("#action" + i)
            .attr("xlink:href", "static/images/0110.gif"); // turn chosen tree orange
        message.style("fill", "lightgray"); // Makes "Choose a grove" text gray

        // rewards = _.zip(d, colors).map(function(x) { // d is the probs for each associated color
        //     return [Math.random() < x[0] ? 1 : 0, x[1]]; // random existence of each color bird based on d
        // });

        //Box-Muller method for sampling from normal (Gaussian) distribution
        normsample = Math.sqrt(-2*Math.log(Math.random()))*Math.cos(2*Math.PI*Math.random());
        reward = normsample * Math.sqrt(d[1][i]) + d[0][i]; // Transform w proper var and mean

        // // Update choices and reward displays
        // var rewarddisplays = rewardgroups.append("g")
        //     .data(rewards);
        // rewarddisplays.each(function (f,k) {
        //     if k === i {
        //         d3.select(this).append('circle')
        //         .attr({
        //         r:25,
        //         cx: 0,
        //         cy: 0,
        //         fill: "#BADBDA",
        //         stroke: "#2F3550",
        //         'stroke-width': 2
        //     });
        //     var label = rewarddisplays.append("text")
        //         .text(reward)
        //         .style("font", "20px monospace")
        //         .attr({
        //             "alignment-baseline": "middle",
        //             "text-anchor": "middle"
        //         })     
        //     }
        

        score = score + reward;
        rewardstodate[i].push(reward)
        // d3.select("#score")
        //     .text(score.toString()); // Replace prev score with new score

        // d3.select("#trial")
        //     .text((ntrials - trial).toString()); // Replace num trials remaining
        scoredisplay = stage.append('text')
            .attr({x: 170, y: 20})
            .text("Reward: " + reward.toString())
            .style("font", "20px monospace");
        scoredisplay.transition()
             .delay(1000)
             .duration(200)
             .style("opacity", 0)
             .remove();

        setTimeout( function () {
            d3.select("#action" + i)
                .attr("xlink:href", "static/images/0810.png");
        }, 1000);

        trialdata = {
            uniqueId: uniqueId,
            condition: EXP.condition,
            counterbalance: EXP.counterbalance,
            phase: "experiment",
            block: params.block,
            blocktrial: trial,
            response: i,
            reward: reward,
            rewardstodate: rewardstodate,
            R: params.R,
            V: params.V,
            swi: params.swi,
            sbw: params.sbw,
            rwdmean: params.rwdmean,
            globaltrial: params.block * EXP.trialsperblock + trial,
            rt: new Date().getTime() - rtTime,
            score: score
        };

        psiTurk.recordTrialData(trialdata);


        // Wait 1200ms before beginning next trial
        setTimeout(next, 1200);
    }

    function transition() {
        psiTurk.showPage("transition.html");
        setTimeout(callback, 5000);
    }

    // *** Will change this part for paytoplay portion 
    function next() {
        trial += 1;

        if (trial > ntrials) { // if end of block
            if (params.block < EXP.nblocks - 1) { // if end of experiment
                transition();
            } else {
                callback();
            }
        } else { // do trial: wait for click on actions, do responseFn, 
            actions.on("click", function (d, i) {responseFn(d, i); });
            message.style("fill", "black");
            rtTime = new Date().getTime();
        }
    }

    psiTurk.showPage("stage.html"); // Blank page for waiting
    setTimeout(setupPage, 1000);
}


function questionnaire() {
    "use strict";
    var errorMessage = "<h1>Oops!</h1><p>Something went wrong submitting your HIT. This might happen if you lose your internet connection. Press the button to resubmit.</p><button id='resubmit'>Resubmit</button>",
        replaceBody, promptResubmit, resubmit, recordResponses;

    replaceBody = function(x) { $("body").html(x); };
    recordResponses = function () {
        psiTurk.recordTrialData({"phase": "postquestionnaire", "status": "submit"});

        $("textarea").each(function () {
            psiTurk.recordUnstructuredData(this.id, this.value);
        });
        $("select").each(function () {
            psiTurk.recordUnstructuredData(this.id, this.value);
        });
    };

    promptResubmit = function () {
        replaceBody(errorMessage);
        $("#resubmit").click(resubmit);
    };

    resubmit = function () {
        var reprompt;
        replaceBody("<h1>Trying to resubmit...</h1>");
        reprompt = setTimeout(promptResubmit, 10000);

        psiTurk.saveData({
            success: function() {
                clearInterval(reprompt);
                psiTurk.computeBonus("compute_bonus", function () {
                    psiTurk.completeHIT();
                });
                // psiTurk.completeHIT();
            },
            error: promptResubmit
        });
    };

    // Load the questionnaire snippet
    psiTurk.showPage("postquestionnaire.html");
    psiTurk.recordTrialData({"phase": "postquestionnaire", "status": "begin"});

    $("#continue").click(function () {
        recordResponses();
        psiTurk.saveData({
            success: function () {
                psiTurk.computeBonus("compute_bonus", function () {
                    psiTurk.completeHIT(); // when finished saving compute bonus, the quit
                });
            },
            error: promptResubmit});
    });
}

function experimentDriver() {
    "use strict";
    var runNext,
        functionList = [],
        paramsList = [];

    runNext = function () {
        var nextFun = functionList.shift(); // nextFun takes the first fn off the list
        if (functionList.length === 0) { // If nextFun was the last fn, it is questionnaire
            nextFun();
        } else {
            // The next function will be decision problem, which requires the inputs params and callback
            nextFun(paramsList.shift(), runNext);
        }
    };

    $.ajax({
        dataType: "json",
        url: "/get_stims", // See custom.py (line 73) and stimuligenerator.py
        data: {condition: EXP.condition,
               counterbalance: EXP.counterbalance,
               nactions: EXP.nactions,
               std_bw: EXP.std_bw,
               std_wi: EXP.std_wi,
               rwdmean: EXP.rwdmean,
               nblocks: EXP.nblocks,
               trialsperblock: EXP.trialsperblock
              },
        success: function (data) {
            EXP.stimuli = data.results; // See custom.py (line 83) 
            /** now EXP.stimuli contains output of stimuligenerator which is array:
            {"R": R,
             "V": V,
             "sbw": sbw,
             "swi": swi,
             "rwdmean":rwdmean,
             "trials": trialsperblock,
             "block": i,
            }
            for each block.
            **/
            console.log(EXP.stimuli);
            paramsList = EXP.stimuli;
            // In below line: EXP.stimuli.length = number of blocks with params to run experiment 
            functionList = _.map(_.range(EXP.stimuli.length), function () {return decisionProblem; });
            functionList.push(questionnaire); // qstnre is at bottom of list, last fn to execute
            runNext(); // Runs fn on top of stack (either decisionproblem or questionnaire)
        }
    });
}



/*******************
 * Run Task
 ******************/
$(window).load(function () {
    "use strict";
    if (EXP.skipinstr) {
        experimentDriver();
    } else {
        psiTurk.doInstructions(
            EXP.instructionPages,
            function () {quiz(EXP.instructionPages, experimentDriver); }
        );
    }
});
