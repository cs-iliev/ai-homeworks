import numpy as np


def generative_model(X_train, Y_train):

    republican_sum = Y_train[Y_train == 1].size
    democrat_sum = Y_train[Y_train == 0].size

    # p(y == 2) and p(y == 0)
    prob_label = np.array(
        [(republican_sum), (democrat_sum)]).reshape(2, 1)
    prob_label = np.true_divide(prob_label, Y_train.size)

    republican_only = X_train[Y_train == 1]
    democrat_only = X_train[Y_train == 0]

    count_republican_votes_yes = np.sum(republican_only, axis=0)
    prob_republican_votes_yes = np.true_divide(
        count_republican_votes_yes, republican_sum)

    count_democrat_votes_yes = np.sum(democrat_only, axis=0)
    prob_democrat_votes_yes = np.true_divide(
        count_democrat_votes_yes, democrat_sum)

    prob_votes = np.array(
        [(prob_republican_votes_yes), (prob_democrat_votes_yes)])

    return prob_label, prob_votes


def discriminative_model(prob_label, prob_votes, X_test):

    mult_by_prob_label_republicans = []
    mult_by_prob_label_democrats = []

    for row in X_test:
        test_var_1 = 1
        test_var_2 = 1
        counter = 0

        for var in row:
            if var == 1:
                test_var_1 = test_var_1 * prob_votes[0, counter]
                test_var_2 = test_var_2 * prob_votes[1, counter]
                counter += 1

            else:
                test_var_1 = test_var_1 * (1 - prob_votes[0, counter])
                test_var_2 = test_var_2 * (1 - prob_votes[1, counter])
                counter += 1

        mult_by_prob_label_republicans.append(test_var_1)
        mult_by_prob_label_democrats.append(test_var_2)

    mult_by_prob_label_republicans = np.asarray(
        mult_by_prob_label_republicans)
    prob_being_republican = mult_by_prob_label_republicans.flatten() * \
        prob_label[0, ]
    mult_by_prob_label_democrats = np.asarray(
        mult_by_prob_label_democrats)
    prob_being_democrat = mult_by_prob_label_democrats.flatten() * \
        prob_label[1, ]

    index = 0
    republicans_over_republicans_and_democrats = []
    democrats_over_republicans_and_democrats = []

    while index < len(prob_being_republican):
        republican_var = prob_being_republican[index] / \
            (prob_being_republican[index]+prob_being_democrat[index])
        democrat_var = prob_being_democrat[index] / \
            (prob_being_republican[index]+prob_being_democrat[index])

        republicans_over_republicans_and_democrats.append(republican_var)
        democrats_over_republicans_and_democrats.append(democrat_var)

        index += 1

    republicans_over_republicans_and_democrats = np.asarray(
        republicans_over_republicans_and_democrats)
    democrats_over_republicans_and_democrats = np.asarray(
        democrats_over_republicans_and_democrats)

    pred_prob = republicans_over_republicans_and_democrats
    return pred_prob


def get_accuracy(Y_true, Y_predicted):

    Y_true = np.asarray(Y_true)
    Y_predicted = np.asarray(Y_predicted)
    Y_true_size = len(Y_true)

    index = 0
    total_correct = 0

    while index < Y_true_size:
        if Y_predicted[index] > .5:
            Y_predicted[index] = 1
        else:
            Y_predicted[index] = 0

        if Y_true[index] == Y_predicted[index]:
            total_correct += 1

        index += 1

    return (total_correct/Y_true_size)*100
