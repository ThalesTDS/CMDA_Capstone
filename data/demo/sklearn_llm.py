from numbers import Real

import numpy as np

from ..base import OutlierMixin, _fit_context
from ..metrics import accuracy_score
from ..utils._param_validation import Interval
from ..utils.validation import check_is_fitted
from ._robust_covariance import MinCovDet


class EllipticEnvelope(OutlierMixin, MinCovDet):
    """
    Identifies outliers by fitting an elliptical boundary around the inlier data.

    This class fits a robust covariance model to the data and uses a threshold
    based on the specified contamination level to separate inliers from outliers.

    Parameters
    ----------
    store_precision : bool, default=True
        Whether to compute and store the precision matrix after fitting.

    assume_centered : bool, default=False
        If True, data is assumed to be centered at the origin.

    support_fraction : float or None, default=None
        Proportion of the dataset used to compute the robust estimate.
        If None, an automatic value is chosen.

    contamination : float, default=0.1
        Expected proportion of outliers in the data (must be in (0, 0.5]).

    random_state : int or None, default=None
        Controls the randomness in the underlying robust covariance estimation.

    Attributes
    ----------
    offset_ : float
        Score threshold separating inliers from outliers.
    """

    def fit(self, X, y=None):
        """
        Fit the robust covariance model and determine the outlier threshold.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training data.

        y : Ignored
            Present for compatibility.

        Returns
        -------
        self : EllipticEnvelope
            Fitted estimator.
        """
        ...

    def decision_function(self, X):
        """
        Compute the raw outlier score for each sample.

        The score is higher for inliers and lower for outliers.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Data to score.

        Returns
        -------
        scores : ndarray of shape (n_samples,)
            Outlier scores relative to the fitted threshold.
        """
        ...

    def score_samples(self, X):
        """
        Return the raw Mahalanobis distance score (negated) for each sample.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Data to evaluate.

        Returns
        -------
        distances : ndarray of shape (n_samples,)
            Negative Mahalanobis distances.
        """
        ...

    def predict(self, X):
        """
        Classify each sample as an inlier or outlier.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Input data.

        Returns
        -------
        labels : ndarray of shape (n_samples,)
            Array with 1 for inliers and -1 for outliers.
        """
        ...

    def score(self, X, y, sample_weight=None):
        """
        Compute the accuracy of predicted labels against true labels.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Input data.

        y : array-like of shape (n_samples,)
            True labels (1 for inliers, -1 for outliers).

        sample_weight : array-like or None, optional
            Optional sample weights.

        Returns
        -------
        accuracy : float
            Classification accuracy.
        """
        ...
