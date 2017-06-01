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
        R = params.R,
        V = params.V,
        ntrials = params.trials,
        trial = 0,
        rtTime,
        names = ["green", "blue", "red"],
        colors = ["green", "blue", "red"];

    function paytoplay() {

    }

    function choicetask(params, callback){
    
    }

    function setupPage() {
        stage = d3.select("body").select("svg");
        message = stage.append("text")
            .attr({x: 170, y: 20})
            .text("Choose a grove")
            .style("font", "20px monospace");

        actiongroups = stage.selectAll(".actionGroup")
            .data(actionmeans)
            .enter()
            .append("g")
            .attr("id", function(d, i) {return "actgroup" + i; })
            .attr("transform", function(d, i) {
                return "translate(" + (50 + 150 * Math.floor(i / 2)) + ", " + (40 + 130 * (i % 2)) + ")";
            });


        actions = actiongroups.append("image")
            .attr("id", function(d, i) {return "action" + i; })
            .attr("class", "action")
            .attr("xlink:href", "static/images/0810.png")
            .attr({width: 100, height: 102});

        actiongroups.append("text")
            .text(function(d, i) {return "Grove " + (i + 1); })
            .attr("x", "20")
            .attr("y", "115");

        stage.append("g")
            .attr("id", "scoregroup")
            .attr("transform", "translate(500, 60)")
            .append("text")
            .text("Birds spotted:")
            .style("font", "24px monospace");

        stage.append("g")
            .attr("id", "trialsgroup") .attr("transform", "translate(500, 150)")
            .append("text")
            .text("Trips in forest:")
            .style("font", "24px monospace");

        d3.select("#scoregroup")
            .append("text")
            .text("0")
            .attr("id", "score")
            .attr("y", 30)
            .style("font", "30px monospace");

        d3.select("#trialsgroup")
            .append("text")
            .text(ntrials - trial)
            .attr("id", "trial")
            .attr("y", 30)
            .style("font", "30px monospace");

        rewardgroups = stage.append("g")
            .attr("transform", "translate(120, 360)")
            .selectAll(".rewardGroup")
            .data(names)
            .enter()
            .append("g")
            .attr("class", "rewardGroup")
            .attr("transform", function(e, j) {
                return "translate(" + (120 * j) + ", 0)";
            });

        rewardgroups.append("text")
            .style("font-size", "20px")
            .style("fill", function(e) {return e; })
            .attr("y", 30)
            .attr({"text-anchor": "end"})
            .text(function(e, j) {return names[j]; });

        next();
    }


    function responseFn(d, i) {
        var rewards,
            rewarddisplays,
            trialdata,
            i,
            j;
        actions.on("click", function () {});
        d3.select("#action" + i)
            .attr("xlink:href", "static/images/0110.gif");
        message.style("fill", "lightgray");

        rewards = _.zip(d, colors).map(function(x) {
            return [Math.random() < x[0] ? 1 : 0, x[1]];
        });

        rewarddisplays = rewardgroups.append("g")
            .data(rewards);
        rewarddisplays.each(function (e) {
            if (e[0] === 1) {
                d3.select(this).append("image")
                    .attr("xlink:href", function(f) {return "static/images/" + f[1] + "bird.png"; })
                    .attr({x: -60, y: -60, width: 80, height: 80});
            }
        });

        score = score + _.reduce(rewards, function(a, b) {return a + b[0]; }, 0);
        d3.select("#score")
            .text(score.toString());

        d3.select("#trial")
            .text((ntrials - trial).toString());

        rewarddisplays.transition()
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
            reward0: rewards[0][0],
            reward1: rewards[1][0],
            reward2: rewards[2][0],
            bestresponse0: params.outcomepairs[0],
            bestresponse1: params.outcomepairs[1],
            bestresponse2: params.outcomepairs[2],
            proportion0: params.proportions[0],
            proportion1: params.proportions[1],
            proportion2: params.proportions[2],
            globaltrial: params.block * EXP.trialsperblock + trial,
            rt: new Date().getTime() - rtTime,
            score: score
        };

        psiTurk.recordTrialData(trialdata);



        setTimeout(next, 1200);
    }

    function transition() {
        psiTurk.showPage("transition.html");
        setTimeout(callback, 5000);
    }

    function next() {
        trial += 1;

        if (trial > ntrials) {
            if (params.block < EXP.nblocks - 1) {
                transition();
            } else {
                callback();
            }
        } else {
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
            /** now EXP.stimuli contains output of stimuligenerator which is:
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
