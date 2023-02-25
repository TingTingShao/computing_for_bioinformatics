% Define lengthMap as a Prolog dict
lengthMap(E, 12) :- E = efficiency.
lengthMap(P, 6) :- P = positioning.
lengthMap(PA, 7) :- PA = polya.

% Define a predicate to calculate the total length of elements and linkers in a terminator.
total_length(Terminator, Length) :-
    total_length(Terminator, 0, Length).

total_length([], Length, Length).
total_length([H|T], Acc, Length) :-
    (   H = element(E)

    %if it is an element, first map element length, then add the length
    ->  lengthMap(E, ElementLength),
        NewAcc is Acc + ElementLength

    %if it is a link, add the length
    ;   H = link(L)
    ->  NewAcc is Acc + L
    ),

    %recursively call total_length method
    total_length(T, NewAcc, Length).

% Define a predicate to calculate score contibuted by the link
link_score(List, Score) :- link_score(List, 0, Score).

link_score([], Score, Score).

% H is the first element, T is the rest of the elements
link_score([H|T], Acc, Score) :-

    % if the first one is the element
    (   H = element(_)

    % score doesn't change
    ->  Acc2 is Acc

    % if the first one is link, and length > 10
    ;   H = link(L), L > 10

    % if link length < 10, score doesn't change
    ->  Acc2 is Acc + 0.5
    ;   H = link(L), L =< 10
    ->  Acc2 is Acc
    ),

    % recursively call link_score function with the rest of the elements
    link_score(T, Acc2, Score).

% Define a predicate to calculate the total number of elements in a terminator.
element_count(Terminator, Count) :- element_count(Terminator, 0, Count).
element_count([], Count, Count).

% H is the first element, T is the rest except for the first one
element_count([H|T], Acc, Count) :-

    % if the first element is element
    (   H = element(_)

    % count + 1
    ->  Acc2 is Acc + 1

    % else, count does not change
    ;   Acc2 is Acc
    ),

    % recursively call method element_count
    element_count(T, Acc2, Count).

%Check whether an element is in terminator or not
check_efficiency(Terminator) :- member(element(efficiency), Terminator).
check_positioning(Terminator) :- member(element(positioning), Terminator).
check_polya(Terminator) :- member(element(polya), Terminator).

%Define a predicate to calculate the score contributed by the last two elements

final_two_elements(Terminator, Score, NewScore) :-
    % Get the final element and linker
    reverse(Terminator, [link(L)|[element(E)|_]]),
    % Check if final element is PA and linker is between 10 and 20 bp
    (   E = polya, L >= 10, L =< 20
    ->  NewScore is Score + 1
    ;   NewScore is Score
    ).

% define the two exceptions for score = 0
terminator_score(Terminator, 0) :-
    %length < 50
    total_length(Terminator, A), A < 50;
    %no elements
    element_count(Terminator, B), B = 0.

% Define a predicate to calculate the terminator score
terminator_score(Terminator, Score) :- terminator_score(Terminator,0,Score).
terminator_score([],Score,Score).
terminator_score(Terminator, Acc, Score) :-
    
    % Calculate the score contributed by elements in the terminator.
       (   check_efficiency(Terminator)
       ->  Acc1 is Acc + 1
       ;   Acc1 is Acc
       ),
    (   check_positioning(Terminator)
    ->  Acc2 is Acc1 + 1
    ;   Acc2 is Acc1
    ),
    (   check_polya(Terminator)
    ->  Acc3 is Acc2 + 1
    ;   Acc3 is Acc2
    ),
    % Calculate the score contributed by linkers in the terminator.
    link_score(Terminator, LinkerScore),
    Acc4 is Acc3 + LinkerScore,

    % Check the final element and linker and update the score if necessary.
    final_two_elements(Terminator, Acc4, Score).
